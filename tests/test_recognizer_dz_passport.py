import pytest
from src.recognizers.dz_passport import DZPassportRecognizer


@pytest.fixture
def rec():
    return DZPassportRecognizer(supported_language="en")


class TestDZPassport:
    def test_valid_9_digit(self, rec):
        results = rec.analyze("Passport 123456789", entities=["DZ_PASSPORT"])
        assert len(results) == 1

    def test_old_format_not_matched(self, rec):
        results = rec.analyze("AB123456", entities=["DZ_PASSPORT"])
        assert len(results) == 0

    def test_too_short(self, rec):
        results = rec.analyze("12345678", entities=["DZ_PASSPORT"])
        assert len(results) == 0
