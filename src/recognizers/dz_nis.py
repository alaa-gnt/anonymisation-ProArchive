from presidio_analyzer import PatternRecognizer, Pattern


class DZNisRecognizer(PatternRecognizer):
    VERSION = "1.0"

    def __init__(self, supported_language: str = None):
        patterns = [
            Pattern(
                "dz_nis",
                r"\b\d{15}\b",
                0.95,
            ),
        ]
        super().__init__(
            supported_entity="DZ_NIS",
            patterns=patterns,
            supported_language=supported_language,
        )
