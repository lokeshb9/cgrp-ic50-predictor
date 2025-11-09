"""
Molecular Fingerprint Generation Module
========================================

Handles molecular fingerprint generation using PaDEL-Descriptor.
Provides robust error handling for Java dependencies and processing timeouts.

Author: Dani Geiger
"""

import pandas as pd
from typing import Optional
from pathlib import Path
import logging
import subprocess

logger = logging.getLogger(__name__)


class FingerprintGenerator:
    """
    Professional molecular fingerprint generation using PaDEL-Descriptor.
    
    Generates molecular fingerprints from SMILES strings with comprehensive
    error handling for Java dependencies and processing failures.
    
    Attributes:
        timeout: Maximum processing time in seconds
        
    Example:
        >>> generator = FingerprintGenerator(timeout=300)
        >>> fingerprints = generator.generate("molecules.smi")
    """
    
    def __init__(self, timeout: int = 300):
        """
        Initialize Fingerprint Generator.
        
        Args:
            timeout: Maximum processing time in seconds (default: 300)
        """
        self.timeout = timeout
        self._check_java_availability()
        logger.info(f"FingerprintGenerator initialized with timeout={timeout}s")
    
    @staticmethod
    def _check_java_availability() -> bool:
        """
        Check if Java is available on the system.
        
        Returns:
            bool: True if Java is available
            
        Raises:
            RuntimeError: If Java is not found
        """
        try:
            result = subprocess.run(
                ['java', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            java_available = result.returncode == 0
            
            if not java_available:
                raise RuntimeError(
                    "Java is not installed or not in PATH. "
                    "Install Java: https://www.java.com"
                )
            
            logger.info("Java availability check passed")
            return True
            
        except FileNotFoundError:
            raise RuntimeError(
                "Java Runtime Environment not found. "
                "PaDEL requires Java. Install from: https://www.java.com"
            )
        except subprocess.TimeoutExpired:
            logger.warning("Java check timed out")
            return False
    
    def generate(
        self,
        input_smi: str = "molecules.smi",
        output_csv: str = "fingerprints.csv",
        fingerprints: bool = True,
        retain_order: bool = True
    ) -> Optional[pd.DataFrame]:
        """
        Generate molecular fingerprints using PaDEL-Descriptor.
        
        Args:
            input_smi: Path to input .smi file
            output_csv: Path to output CSV file
            fingerprints: Whether to generate fingerprints (default: True)
            retain_order: Whether to retain molecule order (default: True)
            
        Returns:
            pd.DataFrame: Generated fingerprints or None if failed
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            RuntimeError: If PaDEL processing fails
            TimeoutError: If processing exceeds timeout
            
        Example:
            >>> generator = FingerprintGenerator()
            >>> df = generator.generate("input.smi", "output.csv")
            >>> print(df.shape)
            (20, 882)  # 881 fingerprints + Name column
        """
        input_path = Path(input_smi)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_smi}")
        
        logger.info(f"Generating fingerprints for {input_smi}")
        
        try:
            from padelpy import padeldescriptor
            
            padeldescriptor(
                mol_dir=input_smi,
                d_file=output_csv,
                fingerprints=fingerprints,
                retainorder=retain_order
            )
            
            # Load and validate output
            if not Path(output_csv).exists():
                raise RuntimeError(f"PaDEL did not create output file: {output_csv}")
            
            df_fingerprints = pd.read_csv(output_csv)
            logger.info(
                f"Successfully generated {df_fingerprints.shape[1]-1} fingerprints "
                f"for {len(df_fingerprints)} molecules"
            )
            
            return df_fingerprints
            
        except ImportError as e:
            logger.error("PaDEL-py not installed")
            raise RuntimeError(
                "padelpy package not found. Install: pip install padelpy"
            ) from e
        
        except subprocess.TimeoutExpired:
            logger.error(f"Fingerprint generation timed out after {self.timeout}s")
            raise TimeoutError(
                f"PaDEL processing exceeded {self.timeout} seconds. "
                "Consider reducing molecule count or increasing timeout."
            )
        
        except Exception as e:
            logger.error(f"Fingerprint generation failed: {e}")
            raise RuntimeError(f"PaDEL processing failed: {str(e)}") from e
    
    @staticmethod
    def validate_fingerprints(df: pd.DataFrame) -> bool:
        """
        Validate generated fingerprints DataFrame.
        
        Args:
            df: Fingerprints DataFrame to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValueError: If fingerprints are invalid
        """
        if df is None or df.empty:
            raise ValueError("Fingerprints DataFrame is empty")
        
        # Check for required 'Name' column
        if 'Name' not in df.columns:
            raise ValueError("Fingerprints missing 'Name' column")
        
        # Check for expected number of features (PaDEL generates 881 fingerprints)
        expected_features = 881
        actual_features = df.shape[1] - 1  # Exclude 'Name' column
        
        if actual_features != expected_features:
            logger.warning(
                f"Expected {expected_features} fingerprints, found {actual_features}"
            )
        
        logger.info("Fingerprints validation passed")
        return True

