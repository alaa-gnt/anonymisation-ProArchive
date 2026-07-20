from presidio_anonymizer import AnonymizerEngine, OperatorConfig


def setup_compliance_anonymizer():
    return AnonymizerEngine()


def _build_operators():
    return {
        # Person names → full placeholder
        "PERSON": OperatorConfig("replace", {"new_value": "<ALGERIAN_CITIZEN>"}),
        # Emails → SHA-256 (traceable without leaking)
        "EMAIL_ADDRESS": OperatorConfig("hash", {"hash_type": "sha256"}),
        # Phone → mask inner digits
        "DZ_PHONE": OperatorConfig("mask", {
            "masking_char": "*",
            "chars_to_mask": 6,
            "from_end": False,
        }),
        # National ID → redact completely
        "DZ_NIN": OperatorConfig("replace", {"new_value": "<ID_REDACTED>"}),
        # Passport → redact
        "DZ_PASSPORT": OperatorConfig("replace", {"new_value": "<PASSPORT_REDACTED>"}),
        # Bank account → mask last 4 digits only
        "DZ_RIB": OperatorConfig("mask", {
            "masking_char": "*",
            "chars_to_mask": 16,
            "from_end": True,
        }),
        # Commercial register → redact
        "DZ_RC": OperatorConfig("replace", {"new_value": "<RC_REDACTED>"}),
        # Tax ID → redact
        "DZ_NIF": OperatorConfig("replace", {"new_value": "<NIF_REDACTED>"}),
        # Social Security Number → redact
        "DZ_SSN": OperatorConfig("replace", {"new_value": "<SSN_REDACTED>"}),
        # Wilaya code → redact
        "DZ_WILAYA": OperatorConfig("replace", {"new_value": "<WILAYA_REDACTED>"}),
        # Postal code → mask
        "DZ_POSTAL": OperatorConfig("mask", {
            "masking_char": "*",
            "chars_to_mask": 3,
            "from_end": False,
        }),
        # General fallback
        "PHONE_NUMBER": OperatorConfig("mask", {
            "masking_char": "*",
            "chars_to_mask": 6,
            "from_end": False,
        }),
        "CREDIT_CARD": OperatorConfig("replace", {"new_value": "<CARD_REDACTED>"}),
        "LOCATION": OperatorConfig("replace", {"new_value": "<LOCATION_REDACTED>"}),
        "DATE_TIME": OperatorConfig("replace", {"new_value": "<DATE_REDACTED>"}),
        "IBAN_CODE": OperatorConfig("replace", {"new_value": "<IBAN_REDACTED>"}),
        "IP_ADDRESS": OperatorConfig("replace", {"new_value": "<IP_REDACTED>"}),
        "URL": OperatorConfig("replace", {"new_value": "<URL_REDACTED>"}),
        "NRP": OperatorConfig("replace", {"new_value": "<NRP_REDACTED>"}),
    }


def run_anonymizer(anonymizer_engine, text_input, analyzer_results):
    operators = _build_operators()

    anonymized_result = anonymizer_engine.anonymize(
        text=text_input,
        analyzer_results=analyzer_results,
        operators=operators,
    )

    return anonymized_result
