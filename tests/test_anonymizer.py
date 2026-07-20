"""
Tests for the anonymisation engine (src/anonymizer.py).
"""

import pytest
from src.analyzer import setup_compliance_analyzer, run_analyzer
from src.anonymizer import (
    setup_compliance_anonymizer,
    run_anonymizer,
    _build_operators,
    anonymize_with_pseudonyms,
)


@pytest.fixture
def analyzer():
    return setup_compliance_analyzer()


@pytest.fixture
def anonymizer():
    return setup_compliance_anonymizer()


class TestAnonymizer:
    def test_person_pseudonymized(self, analyzer):
        text = "Karim a appelé Ahmed et Karim est d'accord."
        results = run_analyzer(analyzer, text, language="fr")
        ops = _build_operators()
        output = anonymize_with_pseudonyms(text, results, ops)
        assert "<PERSON_1>" in output
        assert "<PERSON_2>" in output
        assert output.count("<PERSON_1>") == 2
        assert "Karim" not in output
        assert "Ahmed" not in output

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

    def test_nin_redacted(self, analyzer, anonymizer):
        text = "ID: 123456 123456 123453"
        results = run_analyzer(analyzer, text)
        output = run_anonymizer(anonymizer, text, results)
        assert "<ID_REDACTED>" in output.text

    def test_rib_masked(self, analyzer, anonymizer):
        text = "RIB: 00712345678910001252"
        results = run_analyzer(analyzer, text)
        output = run_anonymizer(anonymizer, text, results)
        assert "****" in output.text

    def test_no_entities_unchanged(self, analyzer, anonymizer):
        text = "Just a normal day."
        results = run_analyzer(analyzer, text)
        output = run_anonymizer(anonymizer, text, results)
        assert output.text == text
