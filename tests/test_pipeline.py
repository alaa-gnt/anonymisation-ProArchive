"""
Tests for the pipeline orchestrator (src/pipeline.py) + ingestion.
"""

import pytest
from src.pipeline import anonymize, anonymize_file
from ingestion import UnsupportedFormatError


class TestPipeline:
    def test_anonymize_returns_result(self):
        result = anonymize("Contact Mehdi at mehdi@example.com")
        assert hasattr(result, "text")
        assert "<PERSON_1>" in result.text

    def test_anonymize_no_pii_returns_string(self):
        result = anonymize("Nothing sensitive here.")
        assert isinstance(result, str)
        assert result == "Nothing sensitive here."

    def test_anonymize_file_txt(self, tmp_path):
        doc = tmp_path / "test.txt"
        doc.write_text("Mr. Mehdi Benali — 0551234567")

        result, meta = anonymize_file(str(doc))
        output = result.text if hasattr(result, "text") else result
        assert "<PERSON_1>" in output
        assert "******" in output
        assert meta["extension"] == ".txt"

    def test_anonymize_file_unsupported_raises(self):
        with pytest.raises(UnsupportedFormatError):
            anonymize_file("nonexistent.xyz")
