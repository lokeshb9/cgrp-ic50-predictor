"""
CGRP Predictor Package
=====================

A production-grade machine learning application for predicting IC50 values 
of CGRP (Calcitonin Gene-Related Peptide) receptor antagonists.

This package provides modular, well-tested components for:
- Molecular data processing
- Fingerprint generation using PaDEL
- IC50 prediction using Random Forest models
- Web-based user interface via Streamlit

Author: Dani Geiger
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Dani Geiger"
__email__ = "dani.geiger@example.com"

from .config import Config
from .predictor import CGRPPredictor
from .data_processor import DataProcessor
from .fingerprint_generator import FingerprintGenerator
from .content_manager import ContentManager, TemplateRenderer

__all__ = [
    "Config",
    "CGRPPredictor",
    "DataProcessor",
    "FingerprintGenerator",
    "ContentManager",
    "TemplateRenderer",
]

