import pytest
from src.recognizers.dz_id_card import DZNINRecognizer


@pytest.fixture
def rec():
    return DZNINRecognizer(supported_language="en")


class TestDZNIN:
    def test_valid_luhn_nin(self, rec):
        results = rec.analyze("NIN 123456 123456 123453", entities=["DZ_NIN"])
        assert len(results) == 1

    def test_invalid_luhn_nin(self, rec):
        results = rec.analyze("NIN 123456 123456 123456", entities=["DZ_NIN"])
        assert len(results) == 0

    def test_too_short(self, rec):
        results = rec.analyze("123456", entities=["DZ_NIN"])
        assert len(results) == 0
