"""
Tests for the anonymisation engine (src/anonymizer.py).
"""

import pytest
from src.analyzer import setup_compliance_analyzer, run_analyzer
from src.anonymizer import setup_compliance_anonymizer, run_anonymizer


@pytest.fixture
def analyzer():
    return setup_compliance_analyzer()


@pytest.fixture
def anonymizer():
    return setup_compliance_anonymizer()


class TestAnonymizer:
    def test_person_replaced(self, analyzer, anonymizer):
        text = "Mr. Mehdi Benali is here."
        results = run_analyzer(analyzer, text)
        output = run_anonymizer(anonymizer, text, results)
        assert "<ALGERIAN_CITIZEN>" in output.text
        assert "Mehdi Benali" not in output.text

    def test_email_hashed(self, analyzer, anonymizer):
        text = "Email: test@example.com"
        results = run_analyzer(analyzer, text)
        output = run_anonymizer(anonymizer, text, results)
        assert "@" not in output.text

    def test_phone_masked(self, analyzer, anonymizer):
        text = "Phone: 0551234567"
        results = run_analyzer(analyzer, text)
        output = run_anonymizer(anonymizer, text, results)
        assert "******" in output.text
        assert "0551234567" not in output.text

    def test_no_entities_unchanged(self, analyzer, anonymizer):
        text = "Just a normal day."
        results = run_analyzer(analyzer, text)
        output = run_anonymizer(anonymizer, text, results)
        assert output.text == text
