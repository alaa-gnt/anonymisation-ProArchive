
from src.analyzer import setup_compliance_analyzer, run_analyzer
from src.anonymizer import setup_compliance_anonymizer, run_anonymizer


# ---------------------------------------------------------------------------
# Singleton references — initialised once on first call to anonymize()
# ---------------------------------------------------------------------------
_analyzer = None
_anonymizer = None


def _ensure_engines(): # calling the userd enginez
    global _analyzer, _anonymizer

    if _analyzer is None:
        _analyzer = setup_compliance_analyzer()

    if _anonymizer is None:
        _anonymizer = setup_compliance_anonymizer()


def anonymize(text_input, language="en"):
    
    # 1. Load engines on first call only
    _ensure_engines()

    # 2. Detect PII entities in the input text
    analyzer_results = run_analyzer(_analyzer, text_input)

    # 3. Exit early if nothing was found
    if not analyzer_results:
        return text_input

    # 4. Anonymise every detected entity using the configured strategies
    anonymized_result = run_anonymizer(
        _anonymizer,
        text_input,
        analyzer_results,
    )

    return anonymized_result
