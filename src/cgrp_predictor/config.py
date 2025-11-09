"""
Configuration Management Module
================================

Centralized configuration management using YAML for production deployment.
Implements singleton pattern for consistent configuration access across the application.

Author: Dani Geiger
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class Config:
    """
    Singleton configuration manager for CGRP Predictor.
    
    Loads and manages application configuration from YAML file,
    providing type-safe access to configuration parameters.
    
    Attributes:
        config_path (Path): Path to the configuration YAML file
        _instance (Config): Singleton instance
        _config (Dict): Loaded configuration dictionary
    
    Example:
        >>> config = Config()
        >>> model_path = config.get_model_path("random_forest")
        >>> threshold = config.get_ic50_threshold("active_max")
    """
    
    _instance: Optional['Config'] = None
    _config: Optional[Dict[str, Any]] = None
    
    def __new__(cls, config_path: Optional[str] = None):
        """
        Implement singleton pattern for configuration.
        
        Args:
            config_path: Path to config YAML file. If None, uses default.
            
        Returns:
            Config: Singleton instance
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize(config_path)
        return cls._instance
    
    def _initialize(self, config_path: Optional[str] = None) -> None:
        """
        Initialize configuration from YAML file.
        
        Args:
            config_path: Path to configuration file
            
        Raises:
            FileNotFoundError: If configuration file doesn't exist
            yaml.YAMLError: If configuration file is invalid
        """
        if config_path is None:
            # Default to config/config.yaml relative to project root
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "config.yaml"
        else:
            config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key.
        
        Args:
            key: Configuration key in dot notation (e.g., 'paths.models_dir')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
            
        Example:
            >>> config.get('app.title')
            'CGRP Receptor Antagonist IC50 Predictor'
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def get_model_path(self, model_name: str) -> Path:
        """
        Get full path to a model file.
        
        Args:
            model_name: Name of model (e.g., 'random_forest', 'scaler')
            
        Returns:
            Path: Full path to model file
            
        Raises:
            KeyError: If model name not found in configuration
        """
        project_root = Path(__file__).parent.parent.parent
        models_dir = self.get('paths.models_dir', 'models')
        model_file = self.get(f'models.{model_name}')
        
        if model_file is None:
            raise KeyError(f"Model '{model_name}' not found in configuration")
        
        return project_root / models_dir / model_file
    
    def get_image_path(self, image_key: str) -> Path:
        """
        Get full path to an image file.
        
        Args:
            image_key: Image key from configuration
            
        Returns:
            Path: Full path to image file
        """
        project_root = Path(__file__).parent.parent.parent
        image_path = self.get(f'images.{image_key}')
        
        if image_path and not Path(image_path).is_absolute():
            return project_root / image_path
        
        return Path(image_path) if image_path else None
    
    def get_ic50_threshold(self, threshold_type: str) -> float:
        """
        Get IC50 classification threshold.
        
        Args:
            threshold_type: Type of threshold ('active_max' or 'intermediate_max')
            
        Returns:
            float: Threshold value in nanomolar (nM)
        """
        return float(self.get(f'predictions.ic50_thresholds.{threshold_type}', 1000))
    
    @property
    def app_title(self) -> str:
        """Get application title."""
        return self.get('app.title', 'CGRP Predictor')
    
    @property
    def app_version(self) -> str:
        """Get application version."""
        return self.get('metadata.version', '1.0.0')
    
    @property
    def variance_threshold(self) -> float:
        """Get variance threshold for feature selection."""
        return float(self.get('processing.variance_threshold', 0.16))
    
    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"Config(version={self.app_version}, models_loaded={self._config is not None})"

