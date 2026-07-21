from presidio_analyzer import PatternRecognizer, Pattern


class DZPassportRecognizer(PatternRecognizer):
    VERSION = "1.0"

    def __init__(self, supported_language: str = None):
        patterns = [
            Pattern(
                "dz_passport",
                r"\b\d{9}\b",
                0.95,
            ),
        ]
        super().__init__(
            supported_entity="DZ_PASSPORT",
            patterns=patterns,
            supported_language=supported_language,
        )
