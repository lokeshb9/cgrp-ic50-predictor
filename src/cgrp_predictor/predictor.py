"""
CGRP IC50 Prediction Module
============================

Main prediction module implementing the complete IC50 prediction pipeline.
Integrates model loading, feature selection, and prediction with robust error handling.

Author: Dani Geiger
"""

import joblib
import pandas as pd
import numpy as np
from typing import Optional, Tuple
from pathlib import Path
import logging

from .config import Config

logger = logging.getLogger(__name__)


class CGRPPredictor:
    """
    Professional IC50 prediction system for CGRP receptor antagonists.
    
    Implements complete prediction pipeline including:
    - Model loading and validation
    - Feature selection via variance threshold
    - IC50 prediction with scaling
    - Classification (active/intermediate/inactive)
    
    Attributes:
        config: Configuration manager
        model: Trained Random Forest model
        scaler: StandardScaler for inverse transformation
        variance_selector: VarianceThreshold feature selector
        
    Example:
        >>> predictor = CGRPPredictor()
        >>> predictions = predictor.predict(fingerprints_df)
        >>> print(predictions['Predicted IC50 (nM)'].head())
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize CGRP Predictor with model loading.
        
        Args:
            config: Configuration instance (creates new if None)
            
        Raises:
            FileNotFoundError: If model files not found
            ValueError: If models fail validation
        """
        self.config = config or Config()
        self.model = None
        self.scaler = None
        self.variance_selector = None
        
        self._load_models()
        logger.info("CGRPPredictor initialized successfully")
    
    def _load_models(self) -> None:
        """
        Load all required model files with validation.
        
        Raises:
            FileNotFoundError: If model files don't exist
            ValueError: If loaded models are invalid
        """
        try:
            # Load Random Forest model
            model_path = self.config.get_model_path('random_forest')
            if not model_path.exists():
                raise FileNotFoundError(f"Model not found: {model_path}")
            
            self.model = joblib.load(model_path)
            logger.info(f"Loaded Random Forest: {self.model.n_estimators} trees")
            
            # Load target scaler
            scaler_path = self.config.get_model_path('scaler')
            if not scaler_path.exists():
                raise FileNotFoundError(f"Scaler not found: {scaler_path}")
            
            self.scaler = joblib.load(scaler_path)
            logger.info("Loaded target scaler")
            
            # Load variance selector
            selector_path = self.config.get_model_path('variance_selector')
            if not selector_path.exists():
                raise FileNotFoundError(f"Variance selector not found: {selector_path}")
            
            self.variance_selector = joblib.load(selector_path)
            logger.info(f"Loaded variance selector: {self.model.n_features_in_} features")
            
            # Validate models
            self._validate_models()
            
        except Exception as e:
            logger.error(f"Model loading failed: {e}")
            raise
    
    def _validate_models(self) -> None:
        """
        Validate loaded models for compatibility and correctness.
        
        Raises:
            ValueError: If models are invalid or incompatible
        """
        if self.model is None:
            raise ValueError("Random Forest model is None")
        
        if not hasattr(self.model, 'predict'):
            raise ValueError("Model doesn't have predict method")
        
        if self.model.n_features_in_ <= 0:
            raise ValueError(f"Invalid feature count: {self.model.n_features_in_}")
        
        logger.info("Model validation passed")
    
    def _apply_variance_threshold(
        self,
        df_fingerprints: pd.DataFrame
    ) -> np.ndarray:
        """
        Apply variance threshold to reduce fingerprint features.
        
        Args:
            df_fingerprints: DataFrame with molecular fingerprints
            
        Returns:
            np.ndarray: Reduced feature matrix
            
        Raises:
            ValueError: If feature selection fails
        """
        # Drop Name column if present
        if 'Name' in df_fingerprints.columns:
            df_features = df_fingerprints.drop(columns=['Name'])
        else:
            df_features = df_fingerprints.copy()
        
        # Ensure numeric types
        df_features = df_features.apply(pd.to_numeric, errors='coerce')
        
        # Check for NaN values
        if df_features.isnull().any().any():
            logger.warning("NaN values detected in fingerprints, filling with 0")
            df_features = df_features.fillna(0)
        
        try:
            X_reduced = self.variance_selector.transform(df_features)
            logger.info(
                f"Features reduced: {df_features.shape[1]} → {X_reduced.shape[1]}"
            )
            return X_reduced
        except Exception as e:
            logger.error(f"Feature selection failed: {e}")
            raise ValueError(f"Variance threshold application failed: {e}")
    
    def _inverse_transform_ic50(
        self,
        predictions: np.ndarray
    ) -> np.ndarray:
        """
        Convert scaled predictions back to IC50 values in nanomolar (nM).
        
        Args:
            predictions: Scaled prediction values
            
        Returns:
            np.ndarray: IC50 values in nM
            
        Note:
            Applies inverse StandardScaler transform, then converts from
            pIC50 (negative log scale) back to IC50 in nanomolar units.
            
            Formula: IC50(nM) = 10^(-pIC50) * 10^9
        """
        try:
            # Inverse scale
            unscaled = self.scaler.inverse_transform(
                predictions.reshape(-1, 1)
            ).flatten()
            
            # Convert from pIC50 to nM
            # pIC50 = -log10(IC50 in Molar)
            # IC50(nM) = 10^(-pIC50) * 10^9
            ic50_nM = 10**(-unscaled) * 10**9
            
            logger.info(
                f"IC50 range: {ic50_nM.min():.2f} - {ic50_nM.max():.2f} nM"
            )
            
            return ic50_nM
            
        except Exception as e:
            logger.error(f"IC50 transformation failed: {e}")
            # Return unscaled if transformation fails
            return predictions
    
    def predict(
        self,
        df_fingerprints: pd.DataFrame,
        include_classification: bool = True
    ) -> pd.DataFrame:
        """
        Predict IC50 values from molecular fingerprints.
        
        Complete prediction pipeline:
        1. Apply variance threshold feature selection
        2. Generate predictions using Random Forest
        3. Inverse transform to IC50 (nM)
        4. Optionally classify as active/intermediate/inactive
        
        Args:
            df_fingerprints: DataFrame with molecular fingerprints
            include_classification: Whether to include activity classification
            
        Returns:
            pd.DataFrame: Predictions with IC50 values (and classification)
            
        Raises:
            ValueError: If prediction fails
            
        Example:
            >>> predictor = CGRPPredictor()
            >>> fingerprints = pd.read_csv("fingerprints.csv")
            >>> results = predictor.predict(fingerprints)
            >>> print(results.columns)
            ['Predicted IC50 (nM)', 'Classification']
        """
        if df_fingerprints is None or df_fingerprints.empty:
            raise ValueError("Fingerprints DataFrame is empty")
        
        logger.info(f"Predicting IC50 for {len(df_fingerprints)} molecules")
        
        try:
            # Apply feature selection
            X_reduced = self._apply_variance_threshold(df_fingerprints)
            
            # Validate feature dimensions
            if X_reduced.shape[1] != self.model.n_features_in_:
                raise ValueError(
                    f"Feature mismatch: model expects {self.model.n_features_in_}, "
                    f"got {X_reduced.shape[1]}"
                )
            
            # Make predictions (scaled)
            predictions_scaled = self.model.predict(X_reduced)
            
            # Convert to IC50 (nM)
            ic50_values = self._inverse_transform_ic50(predictions_scaled)
            
            # Create results DataFrame
            results = pd.DataFrame({
                'Predicted IC50 (nM)': ic50_values
            })
            
            # Add classification if requested
            if include_classification:
                thresholds = {
                    'active_max': self.config.get_ic50_threshold('active_max'),
                    'intermediate_max': self.config.get_ic50_threshold('intermediate_max')
                }
                
                results['Classification'] = results['Predicted IC50 (nM)'].apply(
                    lambda x: self._classify_prediction(x, thresholds)
                )
            
            logger.info("Prediction completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise ValueError(f"Prediction error: {str(e)}") from e
    
    @staticmethod
    def _classify_prediction(ic50: float, thresholds: dict) -> str:
        """
        Classify IC50 prediction into activity category.
        
        Args:
            ic50: IC50 value in nM
            thresholds: Thresholds dict with 'active_max' and 'intermediate_max'
            
        Returns:
            str: Classification ('Active', 'Intermediate', or 'Inactive')
        """
        if ic50 < thresholds['active_max']:
            return 'Active'
        elif ic50 < thresholds['intermediate_max']:
            return 'Intermediate'
        else:
            return 'Inactive'
    
    def get_model_info(self) -> dict:
        """
        Get information about loaded models.
        
        Returns:
            dict: Model information including parameters and metadata
        """
        return {
            'model_type': type(self.model).__name__,
            'n_estimators': self.model.n_estimators if hasattr(self.model, 'n_estimators') else None,
            'n_features': self.model.n_features_in_,
            'config_version': self.config.app_version,
            'variance_threshold': self.config.variance_threshold,
        }
    
    def __repr__(self) -> str:
        """String representation of predictor."""
        model_type = type(self.model).__name__ if self.model else "None"
        n_features = self.model.n_features_in_ if self.model else 0
        return f"CGRPPredictor(model={model_type}, features={n_features})"

