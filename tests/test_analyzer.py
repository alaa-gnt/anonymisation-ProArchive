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

    def test_no_pii_returns_empty(self, analyzer):
        results = run_analyzer(analyzer, "This is a harmless sentence.")
        assert len(results) == 0

    def test_multiple_entities_in_one_text(self, analyzer):
        text = "Mehdi Benali — mehdi@example.com — 0551234567"
        results = run_analyzer(analyzer, text)
        types = {r.entity_type for r in results}
        assert types == {"PERSON", "EMAIL_ADDRESS", "DZ_PHONE"}
