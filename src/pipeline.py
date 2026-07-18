
from src.analyzer import setup_compliance_analyzer, run_analyzer
from src.anonymizer import setup_compliance_anonymizer, run_anonymizer
from ingestion.reader import read_file


# ---------------------------------------------------------------------------
# Singleton references — initialised once on first call to anonymize()
# ---------------------------------------------------------------------------
_analyzer = None
_anonymizer = None


def _ensure_engines():
    """Lazily load the analyzer and anonymizer engines (once)."""
    global _analyzer, _anonymizer

    if _analyzer is None:
        _analyzer = setup_compliance_analyzer()

    if _anonymizer is None:
        _anonymizer = setup_compliance_anonymizer()


def anonymize(text_input, language="en"):
    """
    Analyse *text_input* for PII entities, then anonymise them in-place.

    Parameters
    ----------
    text_input : str
        Raw document text to process.
    language : str, optional
        ISO 639-1 language code (default ``"en"``).

    Returns
    -------
    str or AnonymizerResult
        If entities were found and processed, returns an ``AnonymizerResult``
        with a ``.text`` attribute. If nothing was found, returns the
        original string unchanged.
    """
    _ensure_engines()

    analyzer_results = run_analyzer(_analyzer, text_input)

    if not analyzer_results:
        return text_input

    anonymized_result = run_anonymizer(
        _anonymizer,
        text_input,
        analyzer_results,
    )

    return anonymized_result


def anonymize_file(path, language="en"):
    """
    Read a document from disk and return its anonymised text.

    This is a convenience wrapper around ``read_file()`` + ``anonymize()``.

    Parameters
    ----------
    path : str or Path
        Path to the document (TXT, PDF, DOCX, or image).
    language : str, optional
        ISO 639-1 language code.

    Returns
    -------
    (text, metadata)
        text : str — the anonymised text.
        metadata : dict — source info (filename, extension, char count).
    """
    raw_text, metadata = read_file(path)
    result = anonymize(raw_text, language=language)
    return result, metadata
