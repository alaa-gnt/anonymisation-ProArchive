import pytest
from src.recognizers.dz_phone import DZPhoneRecognizer


@pytest.fixture
def rec():
    return DZPhoneRecognizer(supported_language="en")


class TestDZPhone:
    def test_mobile_valid(self, rec):
        results = rec.analyze("Call 0551234567 now", entities=["DZ_PHONE"])
        assert len(results) == 1
        assert results[0].entity_type == "DZ_PHONE"

    def test_mobile_ooredoo(self, rec):
        results = rec.analyze("0661234567", entities=["DZ_PHONE"])
        assert len(results) == 1

    def test_mobile_djezzy(self, rec):
        results = rec.analyze("0771234567", entities=["DZ_PHONE"])
        assert len(results) == 1

    def test_landline_alger(self, rec):
        results = rec.analyze("021123456", entities=["DZ_PHONE"])
        assert len(results) == 1

    def test_landline_oran(self, rec):
        results = rec.analyze("0411234567", entities=["DZ_PHONE"])
        assert len(results) == 1

    def test_invalid_too_short(self, rec):
        results = rec.analyze("055123", entities=["DZ_PHONE"])
        assert len(results) == 0

    def test_invalid_wrong_prefix(self, rec):
        results = rec.analyze("0812345678", entities=["DZ_PHONE"])
        assert len(results) == 0
