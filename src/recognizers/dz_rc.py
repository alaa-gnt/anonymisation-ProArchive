from presidio_analyzer import PatternRecognizer, Pattern


class DZRcRecognizer(PatternRecognizer):
    VERSION = "1.0"

    def __init__(self, supported_language: str = None):
        patterns = [
            Pattern(
                "dz_rc",
                r"\b\d{2}\s*/\s*(0[1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-8]|5[0-8])\s*-\s*\d{6,8}(\s*[A-Z])?\b",
                0.95,
            ),
        ]
        super().__init__(
            supported_entity="DZ_RC",
            patterns=patterns,
            supported_language=supported_language,
        )
