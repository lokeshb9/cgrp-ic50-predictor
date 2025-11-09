"""
Data Processing Module
======================

Handles molecular data validation, cleaning, and preparation for prediction.
Implements robust error handling and validation for SMILES strings and ChEMBL IDs.

Author: Dani Geiger
"""

import pandas as pd
from typing import Tuple, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Professional data processing for molecular SMILES and ChEMBL IDs.
    
    Provides validated, type-safe data processing with comprehensive error handling
    for molecular input data preparation.
    
    Attributes:
        None
    
    Example:
        >>> processor = DataProcessor()
        >>> chembl_col, smiles_col = processor.detect_columns(df)
        >>> is_valid = processor.validate_smiles("CCO")
    """
    
    def __init__(self):
        """Initialize Data Processor."""
        logger.info("DataProcessor initialized")
    
    @staticmethod
    def detect_columns(df: pd.DataFrame) -> Optional[Tuple[str, str]]:
        """
        Automatically detect ChEMBL ID and SMILES columns in a DataFrame.
        
        Uses heuristics to identify which column contains ChEMBL identifiers
        and which contains SMILES strings based on content patterns.
        
        Args:
            df: DataFrame with exactly 2 columns
            
        Returns:
            Tuple of (chembl_column_name, smiles_column_name) or None if invalid
            
        Raises:
            ValueError: If DataFrame doesn't have exactly 2 columns
            
        Example:
            >>> df = pd.DataFrame({'id': ['CHEMBL123'], 'mol': ['CCO']})
            >>> chembl_col, smiles_col = DataProcessor.detect_columns(df)
            >>> print(chembl_col, smiles_col)
            'id' 'mol'
        """
        if df.shape[1] != 2:
            error_msg = f"Expected 2 columns, found {df.shape[1]}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        col1, col2 = df.columns
        
        # Count ChEMBL-like identifiers in each column
        chembl_count_col1 = df[col1].astype(str).str.startswith("CHEMBL").sum()
        chembl_count_col2 = df[col2].astype(str).str.startswith("CHEMBL").sum()
        
        if chembl_count_col1 > chembl_count_col2:
            chembl_col, smiles_col = col1, col2
        else:
            chembl_col, smiles_col = col2, col1
        
        logger.info(f"Detected columns - ChEMBL: {chembl_col}, SMILES: {smiles_col}")
        return chembl_col, smiles_col
    
    @staticmethod
    def validate_smiles(smiles: str) -> bool:
        """
        Validate a SMILES string using RDKit.
        
        Args:
            smiles: SMILES string to validate
            
        Returns:
            bool: True if valid, False otherwise
            
        Note:
            Requires RDKit to be installed. Falls back to basic validation if unavailable.
            
        Example:
            >>> DataProcessor.validate_smiles("CCO")
            True
            >>> DataProcessor.validate_smiles("invalid")
            False
        """
        if not smiles or not isinstance(smiles, str):
            return False
        
        try:
            from rdkit import Chem
            mol = Chem.MolFromSmiles(smiles)
            is_valid = mol is not None
            logger.debug(f"SMILES validation: {smiles[:20]}... -> {is_valid}")
            return is_valid
        except ImportError:
            # Fallback: basic validation if RDKit not available
            logger.warning("RDKit not available, using basic SMILES validation")
            return len(smiles) > 0 and not smiles.isspace()
        except Exception as e:
            logger.error(f"Error validating SMILES: {e}")
            return False
    
    @staticmethod
    def prepare_smi_file(
        df: pd.DataFrame, 
        output_file: str = "molecules.smi"
    ) -> Optional[str]:
        """
        Prepare a .smi file for PaDEL-Descriptor processing.
        
        Extracts SMILES and molecular IDs, saves in tab-separated format
        required by PaDEL.
        
        Args:
            df: DataFrame containing ChEMBL IDs and SMILES
            output_file: Output filename for .smi file
            
        Returns:
            str: Path to created .smi file, or None if failed
            
        Raises:
            ValueError: If column detection fails
            IOError: If file cannot be written
            
        Example:
            >>> df = pd.DataFrame({'id': ['CHEMBL1'], 'smiles': ['CCO']})
            >>> processor = DataProcessor()
            >>> smi_path = processor.prepare_smi_file(df)
        """
        try:
            chembl_col, smiles_col = DataProcessor.detect_columns(df)
            
            # PaDEL format: SMILES first, then ID
            df_smi = df[[smiles_col, chembl_col]]
            df_smi.to_csv(output_file, sep='\t', index=False, header=False)
            
            logger.info(f"Created .smi file: {output_file} with {len(df)} molecules")
            return output_file
            
        except ValueError as e:
            logger.error(f"Column detection failed: {e}")
            return None
        except IOError as e:
            logger.error(f"Failed to write .smi file: {e}")
            return None
    
    @staticmethod
    def read_input_file(
        file_path: str,
        expected_columns: int = 2
    ) -> pd.DataFrame:
        """
        Read and validate input CSV/TXT file.
        
        Intelligently detects separators and validates column count.
        
        Args:
            file_path: Path to input file
            expected_columns: Expected number of columns (default: 2)
            
        Returns:
            pd.DataFrame: Validated DataFrame
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If column count doesn't match expected
            
        Example:
            >>> df = DataProcessor.read_input_file("molecules.csv")
            >>> print(df.shape)
            (20, 2)
        """
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        
        try:
            # Auto-detect separator
            df = pd.read_csv(file_path, sep=None, engine="python", header=None)
            
            if df.shape[1] != expected_columns:
                raise ValueError(
                    f"Expected {expected_columns} columns, found {df.shape[1]}"
                )
            
            logger.info(f"Successfully read {len(df)} rows from {file_path}")
            return df
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise
    
    @staticmethod
    def classify_ic50(ic50_value: float, thresholds: dict = None) -> str:
        """
        Classify IC50 value into activity categories.
        
        Args:
            ic50_value: IC50 value in nanomolar (nM)
            thresholds: Custom thresholds dict with 'active_max' and 'intermediate_max'
            
        Returns:
            str: Classification ('active', 'intermediate', or 'inactive')
            
        Example:
            >>> DataProcessor.classify_ic50(500)
            'active'
            >>> DataProcessor.classify_ic50(5000)
            'intermediate'
            >>> DataProcessor.classify_ic50(15000)
            'inactive'
        """
        if thresholds is None:
            thresholds = {'active_max': 1000, 'intermediate_max': 10000}
        
        if ic50_value < thresholds['active_max']:
            return 'active'
        elif ic50_value < thresholds['intermediate_max']:
            return 'intermediate'
        else:
            return 'inactive'

