"""
Unit Tests for Data Processor
==============================

Tests for data processing, validation, and SMILES handling.

Author: Dani Geiger
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from cgrp_predictor.data_processor import DataProcessor


class TestDataProcessor:
    """Test suite for DataProcessor class."""
    
    @pytest.fixture
    def processor(self):
        """Create DataProcessor instance."""
        return DataProcessor()
    
    @pytest.fixture
    def valid_dataframe(self):
        """Create valid test DataFrame."""
        return pd.DataFrame({
            'ChEMBL_ID': ['CHEMBL123', 'CHEMBL456'],
            'SMILES': ['CCO', 'CC(=O)O']
        })
    
    def test_detect_columns_valid(self, valid_dataframe):
        """Test column detection with valid input."""
        chembl_col, smiles_col = DataProcessor.detect_columns(valid_dataframe)
        assert chembl_col == 'ChEMBL_ID'
        assert smiles_col == 'SMILES'
    
    def test_detect_columns_reversed(self):
        """Test column detection with reversed columns."""
        df = pd.DataFrame({
            'mol': ['CCO', 'CC(=O)O'],
            'id': ['CHEMBL123', 'CHEMBL456']
        })
        chembl_col, smiles_col = DataProcessor.detect_columns(df)
        assert chembl_col == 'id'
        assert smiles_col == 'mol'
    
    def test_detect_columns_invalid_shape(self):
        """Test column detection with wrong number of columns."""
        df = pd.DataFrame({
            'a': [1, 2],
            'b': [3, 4],
            'c': [5, 6]
        })
        with pytest.raises(ValueError, match="Expected 2 columns"):
            DataProcessor.detect_columns(df)
    
    def test_validate_smiles_valid(self):
        """Test SMILES validation with valid molecules."""
        assert DataProcessor.validate_smiles("CCO") == True
        assert DataProcessor.validate_smiles("c1ccccc1") == True
        assert DataProcessor.validate_smiles("CC(=O)O") == True
    
    def test_validate_smiles_invalid(self):
        """Test SMILES validation with invalid molecules."""
        assert DataProcessor.validate_smiles("not_a_smiles") == False
        assert DataProcessor.validate_smiles("") == False
        assert DataProcessor.validate_smiles(None) == False
    
    def test_classify_ic50_active(self):
        """Test IC50 classification for active compounds."""
        result = DataProcessor.classify_ic50(500)
        assert result == 'active'
    
    def test_classify_ic50_intermediate(self):
        """Test IC50 classification for intermediate compounds."""
        result = DataProcessor.classify_ic50(5000)
        assert result == 'intermediate'
    
    def test_classify_ic50_inactive(self):
        """Test IC50 classification for inactive compounds."""
        result = DataProcessor.classify_ic50(15000)
        assert result == 'inactive'
    
    def test_classify_ic50_boundary_active(self):
        """Test IC50 classification at active boundary."""
        result = DataProcessor.classify_ic50(999)
        assert result == 'active'
    
    def test_classify_ic50_boundary_intermediate(self):
        """Test IC50 classification at intermediate boundary."""
        result = DataProcessor.classify_ic50(9999)
        assert result == 'intermediate'
    
    def test_prepare_smi_file(self, processor, valid_dataframe, tmp_path):
        """Test .smi file preparation."""
        output_file = tmp_path / "test.smi"
        result = processor.prepare_smi_file(valid_dataframe, str(output_file))
        
        assert result is not None
        assert output_file.exists()
        
        # Verify content
        content = output_file.read_text()
        assert 'CCO' in content
        assert 'CHEMBL123' in content

