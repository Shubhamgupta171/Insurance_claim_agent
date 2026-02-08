"""
Unit tests for the PDF extractor module.
"""

import pytest
from pathlib import Path
from src.extractor import PDFExtractor
from src.models import ClaimData


class TestPDFExtractor:
    """Test cases for PDFExtractor"""
    
    @pytest.fixture
    def extractor(self):
        """Create extractor instance without AI"""
        return PDFExtractor(use_ai=False)
    
    def test_extractor_initialization(self, extractor):
        """Test that extractor initializes correctly"""
        assert extractor is not None
        assert extractor.use_ai == False
    
    def test_extract_text_from_pdf(self, extractor):
        """Test text extraction from PDF"""
        # This test requires actual PDF files
        # Will work after PDFs are generated
        pass
    
    def test_extract_with_regex(self, extractor):
        """Test regex-based extraction"""
        sample_text = """
        POLICY NUMBER: POL-123456
        DATE OF LOSS: 02/01/2026
        V.I.N.: 1HGBH41JXMN109186
        ESTIMATE AMOUNT: $12,500.00
        """
        
        result = extractor.extract_with_regex(sample_text)
        
        assert 'policy_number' in result
        assert result['policy_number'] == 'POL-123456'
        assert 'estimated_damage' in result
        assert result['estimated_damage'] == 12500.0
    
    def test_extract_from_pdf_returns_claim_data(self, extractor):
        """Test that extraction returns ClaimData object"""
        # This test requires actual PDF files
        pass
