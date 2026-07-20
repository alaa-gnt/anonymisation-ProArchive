"""
Tests for the PII detection engine (src/analyzer.py).
"""

import pytest
from src.analyzer import setup_compliance_analyzer, run_analyzer


@pytest.fixture
def analyzer():
    return setup_compliance_analyzer()


class TestAnalyzer:
    def test_detect_person(self, analyzer):
        results = run_analyzer(analyzer, "Mehdi Benali lives in Algiers.")
        types = [r.entity_type for r in results]
        assert "PERSON" in types

    def test_detect_email(self, analyzer):
        results = run_analyzer(analyzer, "contact me at test@example.com")
        types = [r.entity_type for r in results]
        assert "EMAIL_ADDRESS" in types

    def test_detect_algerian_phone(self, analyzer):
        results = run_analyzer(analyzer, "Call me on 0551234567")
        types = [r.entity_type for r in results]
        assert "DZ_PHONE" in types

    def test_detect_nin(self, analyzer):
        results = run_analyzer(analyzer, "My ID is 123456 123456 123456")
        types = [r.entity_type for r in results]
        assert "DZ_NIN" in types

    def test_detect_passport(self, analyzer):
        results = run_analyzer(analyzer, "Passport AB123456")
        types = [r.entity_type for r in results]
        assert "DZ_PASSPORT" in types

    def test_detect_rib(self, analyzer):
        results = run_analyzer(analyzer, "RIB: 00712345678910001234")
        types = [r.entity_type for r in results]
        assert "DZ_RIB" in types

    def test_detect_rc(self, analyzer):
        results = run_analyzer(analyzer, "RC: B1234567890")
        types = [r.entity_type for r in results]
        assert "DZ_RC" in types

    def test_detect_nif(self, analyzer):
        results = run_analyzer(analyzer, "NIF: 123456789012345")
        types = [r.entity_type for r in results]
        assert "DZ_NIF" in types

    def test_detect_postal(self, analyzer):
        results = run_analyzer(analyzer, "Alger 16000")
        types = [r.entity_type for r in results]
        assert "DZ_POSTAL" in types

    def test_no_pii_returns_empty(self, analyzer):
        results = run_analyzer(analyzer, "This is a harmless sentence.")
        assert len(results) == 0

    def test_multiple_entities_in_one_text(self, analyzer):
        text = "Mehdi Benali — mehdi@example.com — 0551234567 — 123456 123456 123456"
        results = run_analyzer(analyzer, text)
        types = {r.entity_type for r in results}
        assert "PERSON" in types
        assert "EMAIL_ADDRESS" in types
        assert "DZ_PHONE" in types
        assert "DZ_NIN" in types
