"""
Unit Tests for Configuration Module
====================================

Tests for configuration loading and management.

Author: Dani Geiger
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from cgrp_predictor.config import Config


class TestConfig:
    """Test suite for Config class."""
    
    def test_config_singleton(self):
        """Test that Config implements singleton pattern."""
        config1 = Config()
        config2 = Config()
        assert config1 is config2
    
    def test_config_loads(self):
        """Test that configuration loads successfully."""
        config = Config()
        assert config._config is not None
        assert isinstance(config._config, dict)
    
    def test_get_simple_value(self):
        """Test getting simple configuration value."""
        config = Config()
        title = config.get('app.title')
        assert title is not None
        assert isinstance(title, str)
    
    def test_get_with_default(self):
        """Test getting value with default."""
        config = Config()
        result = config.get('nonexistent.key', 'default_value')
        assert result == 'default_value'
    
    def test_get_nested_value(self):
        """Test getting nested configuration value."""
        config = Config()
        threshold = config.get('processing.variance_threshold')
        assert threshold is not None
        assert isinstance(threshold, float)
    
    def test_app_title_property(self):
        """Test app_title property."""
        config = Config()
        assert config.app_title is not None
        assert isinstance(config.app_title, str)
    
    def test_app_version_property(self):
        """Test app_version property."""
        config = Config()
        assert config.app_version is not None
        assert isinstance(config.app_version, str)
    
    def test_variance_threshold_property(self):
        """Test variance_threshold property."""
        config = Config()
        threshold = config.variance_threshold
        assert isinstance(threshold, float)
        assert 0 < threshold < 1
    
    def test_get_ic50_threshold_active(self):
        """Test getting IC50 active threshold."""
        config = Config()
        threshold = config.get_ic50_threshold('active_max')
        assert isinstance(threshold, float)
        assert threshold == 1000.0
    
    def test_get_ic50_threshold_intermediate(self):
        """Test getting IC50 intermediate threshold."""
        config = Config()
        threshold = config.get_ic50_threshold('intermediate_max')
        assert isinstance(threshold, float)
        assert threshold == 10000.0
    
    def test_repr(self):
        """Test string representation."""
        config = Config()
        repr_str = repr(config)
        assert 'Config' in repr_str
        assert 'version' in repr_str.lower()

