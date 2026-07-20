import pytest
from src.recognizers.dz_rc import DZRcRecognizer


@pytest.fixture
def rec():
    return DZRcRecognizer(supported_language="en")


class TestDZRC:
    def test_separated_format(self, rec):
        results = rec.analyze("RC 16/16-0123456", entities=["DZ_RC"])
        assert len(results) == 1

    def test_with_legal_letter(self, rec):
        results = rec.analyze("RC 16/16-0123456 B", entities=["DZ_RC"])
        assert len(results) == 1

    def test_different_wilaya(self, rec):
        results = rec.analyze("22/31-12345678", entities=["DZ_RC"])
        assert len(results) == 1

    def test_invalid_wilaya(self, rec):
        results = rec.analyze("16/99-0123456", entities=["DZ_RC"])
        assert len(results) == 0

    def test_compact_phone_not_matched(self, rec):
        results = rec.analyze("0551234567", entities=["DZ_RC"])
        assert len(results) == 0
