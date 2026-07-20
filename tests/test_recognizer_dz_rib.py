import pytest
from src.recognizers.dz_rib import DZRIbRecognizer


@pytest.fixture
def rec():
    return DZRIbRecognizer(supported_language="en")


class TestDZRIB:
    def test_valid_rib(self, rec):
        results = rec.analyze("RIB 00712345678910001252", entities=["DZ_RIB"])
        assert len(results) == 1

    def test_invalid_rib(self, rec):
        results = rec.analyze("RIB 00712345678910001234", entities=["DZ_RIB"])
        assert len(results) == 0

    def test_too_short(self, rec):
        results = rec.analyze("1234567890", entities=["DZ_RIB"])
        assert len(results) == 0
