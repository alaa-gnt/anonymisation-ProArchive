from presidio_analyzer import PatternRecognizer, Pattern, RecognizerResult

from ._checksums import is_valid_iban


class DZIbanRecognizer(PatternRecognizer):
    VERSION = "1.0"

    def __init__(self, supported_language: str = None):
        patterns = [
            Pattern(
                "dz_iban",
                r"\bDZ\d{22}\b",
                0.95,
            ),
        ]
        super().__init__(
            supported_entity="IBAN_CODE",
            patterns=patterns,
            supported_language=supported_language,
        )

    def analyze(self, text, entities, nlp_artifacts=None):
        results = super().analyze(text, entities, nlp_artifacts)
        return [
            r for r in results
            if is_valid_iban(text[r.start:r.end])
        ]
