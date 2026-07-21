from presidio_analyzer import PatternRecognizer, Pattern


class DZNifRecognizer(PatternRecognizer):
    VERSION = "1.0"

    def __init__(self, supported_language: str = None):
        patterns = [
            Pattern(
                "dz_nif",
                r"\b\d{15}\b",
                0.95,
            ),
        ]
        super().__init__(
            supported_entity="DZ_NIF",
            patterns=patterns,
            supported_language=supported_language,
        )
