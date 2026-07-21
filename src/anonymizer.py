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
        # Tax ID (NIS) → redact
        "DZ_NIS": OperatorConfig("replace", {"new_value": "<NIS_REDACTED>"}),
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


def _apply_operator(value, config):
    """Apply a single operator to *value* and return the transformed string."""
    if config is None:
        return value

    op = config.operator_name
    params = config.params or {}

    if op == "replace":
        return params.get("new_value", value)

    if op == "hash":
        import hashlib
        h = hashlib.new(params.get("hash_type", "sha256"))
        h.update(value.encode("utf-8"))
        return h.hexdigest()

    if op == "mask":
        char = params.get("masking_char", "*")
        n = params.get("chars_to_mask", 0)
        if params.get("from_end", True):
            keep = value[:max(0, len(value) - n)]
            return keep + char * min(n, len(value))
        else:
            keep = value[min(n, len(value)):]
            return char * min(n, len(value)) + keep

    if op == "redact":
        return ""

    return value


def anonymize_with_pseudonyms(text, analyzer_results, operators):
    """Replace PII entities with context-dependent operators.

    * PERSON → ``<PERSON_1>``, ``<PERSON_2>`` …  (one index per unique name).
    * Everything else → uses the operator defined in *operators*.

    Applies replacements **right-to-left** so original text offsets stay valid.
    """
    groups = {}
    for r in analyzer_results:
        if r.entity_type == "PERSON":
            val = text[r.start:r.end]
            first = val.split()[0] if val.split() else val
            groups.setdefault(first, set()).add(val)

    assignments = {}
    for idx, vals in enumerate(groups.values(), 1):
        tag = f"<PERSON_{idx}>"
        for v in vals:
            assignments[v] = tag

    sorted_results = sorted(analyzer_results, key=lambda r: -r.start)

    result = text
    for r in sorted_results:
        original = text[r.start:r.end]

        if r.entity_type == "PERSON":
            replacement = assignments[original]
        else:
            cfg = operators.get(r.entity_type)
            replacement = _apply_operator(original, cfg)

        result = result[:r.start] + replacement + result[r.end:]

    return result


def run_anonymizer(anonymizer_engine, text_input, analyzer_results):
    operators = _build_operators()

    anonymized_result = anonymizer_engine.anonymize(
        text=text_input,
        analyzer_results=analyzer_results,
        operators=operators,
    )

    return anonymized_result
