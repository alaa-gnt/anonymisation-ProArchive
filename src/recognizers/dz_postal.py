from presidio_analyzer import PatternRecognizer, Pattern


class DZPostalRecognizer(PatternRecognizer):
    VERSION = "1.0"

    def __init__(self, supported_language: str = None):
        patterns = [
            Pattern(
                "dz_postal",
                r"\b(0[1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-8]|5[0-8])\d{3}\b",
                0.85,
            ),
        ]
        super().__init__(
            supported_entity="DZ_POSTAL",
            patterns=patterns,
            supported_language=supported_language,
        )
