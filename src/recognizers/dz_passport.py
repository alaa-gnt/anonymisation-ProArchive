import re

from presidio_analyzer import PatternRecognizer, Pattern, RecognizerResult


_PASSPORT_CONTEXT = {
    "passeport", "passport", "pasport",
    "جواز", "جواز سفر",
    "PASSPORT", "PASSEPORT",
    "travel document", "document de voyage",
    "passeport n°", "passport no", "passport num",
    "n° passeport", "n. passeport",
    "numéro de passeport", "numéro passeport",
    "رقم الجواز",
}


class DZPassportRecognizer(PatternRecognizer):
    VERSION = "1.0"

    def __init__(self, supported_language: str = None):
        patterns = [
            # Old format: 2 letters + 6 digits (e.g., AB123456)
            Pattern(
                "dz_passport_old",
                r"\b[A-Za-z]{2}\d{6}\b",
                0.95,
            ),
            # New biometric format: 9 digits — low base score,
            # boosted in analyze() when passport context is nearby
            Pattern(
                "dz_passport_digital",
                r"\b\d{9}\b",
                0.40,
            ),
        ]
        super().__init__(
            supported_entity="DZ_PASSPORT",
            patterns=patterns,
            supported_language=supported_language,
        )

    def analyze(self, text, entities, nlp_artifacts=None):
        results = super().analyze(text, entities, nlp_artifacts)
        if not results:
            return results

        window = 50
        filtered = []
        for r in results:
            snippet = text[r.start:r.end]
            # 2-letter + 6-digit format — always high confidence
            if re.match(r"^[A-Za-z]{2}\d{6}$", snippet):
                filtered.append(
                    RecognizerResult(r.entity_type, r.start, r.end, 0.95)
                )
                continue

            # 9-digit format — check context
            before = text[max(0, r.start - window):r.start].lower()
            after = text[r.end:min(len(text), r.end + window)].lower()
            nearby = before + after

            has_context = any(ctx.lower() in nearby for ctx in _PASSPORT_CONTEXT)
            if has_context:
                filtered.append(
                    RecognizerResult(r.entity_type, r.start, r.end, 0.95)
                )
            else:
                filtered.append(
                    RecognizerResult(r.entity_type, r.start, r.end, 0.30)
                )

        return filtered
