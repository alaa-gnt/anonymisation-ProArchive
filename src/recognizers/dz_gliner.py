from presidio_analyzer.predefined_recognizers import GLiNERRecognizer


class DZGlinerRecognizer(GLiNERRecognizer):
    VERSION = "1.0"

    def __init__(self, supported_language: str = None):
        entity_mapping = {
            "national id number": "DZ_NIN",
            "passport number": "DZ_PASSPORT",
            "phone number": "DZ_PHONE",
            "email address": "EMAIL_ADDRESS",
            "iban": "IBAN_CODE",
            "bank account number": "DZ_RIB",
        }
        super().__init__(
            supported_language=supported_language or "en",
            entity_mapping=entity_mapping,
            model_name="urchade/gliner_multi_pii-v1",
            threshold=0.35,
        )
