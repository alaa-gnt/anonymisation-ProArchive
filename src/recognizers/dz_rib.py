from presidio_analyzer import PatternRecognizer, Pattern, RecognizerResult

from ._checksums import is_valid_rib


class DZRIbRecognizer(PatternRecognizer):
    VERSION = "1.0"

    def __init__(self, supported_language: str = None):
        patterns = [
            Pattern(
                "dz_rib",
                r"\b\d{20}\b",
                0.95,
            ),
        ]
        super().__init__(
            supported_entity="DZ_RIB",
            patterns=patterns,
            supported_language=supported_language,
        )

    def analyze(self, text, entities, nlp_artifacts=None):
        results = super().analyze(text, entities, nlp_artifacts)
        return [
            r for r in results
            if is_valid_rib(text[r.start:r.end])
        ]
