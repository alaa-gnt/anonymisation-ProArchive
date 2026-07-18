from presidio_anonymizer import AnonymizerEngine, OperatorConfig


def setup_compliance_anonymizer():
    return AnonymizerEngine()


def run_anonymizer(anonymizer_engine, text_input, analyzer_results):
    operators = {
        "PERSON": OperatorConfig("replace", {"new_value": "<ALGERIAN_CITIZEN>"}),
        "EMAIL_ADDRESS": OperatorConfig("hash", {"hash_type": "sha256"}),
        "DZ_PHONE": OperatorConfig("mask", {
            "masking_char": "*",
            "chars_to_mask": 6,
            "from_end": False,
        }),
    }

    anonymized_result = anonymizer_engine.anonymize(
        text=text_input,
        analyzer_results=analyzer_results,
        operators=operators,
    )

    return anonymized_result