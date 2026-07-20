
import unicodedata
from langdetect import detect as detect_lang

from src.analyzer import setup_compliance_analyzer, run_analyzer
from src.anonymizer import _build_operators, anonymize_with_pseudonyms
from ingestion.reader import read_file


# ---------------------------------------------------------------------------
# Singleton reference — initialized once on first call to anonymize()
# ---------------------------------------------------------------------------
_analyzer = None


def _ensure_engines():
    global _analyzer

    if _analyzer is None:
        _analyzer = setup_compliance_analyzer()


_SUPPORTED_LANGUAGES = {"en", "fr", "ar"}


def _detect_language(text):
    try:
        lang = detect_lang(text)
        return lang if lang in _SUPPORTED_LANGUAGES else "en"
    except Exception:
        return "en"


def _has_arabic(text):
    return any(0x0600 <= ord(c) <= 0x06FF for c in text)


def _has_latin(text):
    return any(
        unicodedata.name(c, "").startswith("LATIN")
        for c in text
    )


def _merge_results(*result_lists, full_text=""):
    """Merge results from multiple language pipelines.

    Rules
    -----
    * Overlapping spans → keep the highest score.
    * Equal score → keep the longer span (more complete entity).
    * Cross-language NER false positives are discarded:
      - French/English NER entities on Arabic-script text are dropped.
      - Arabic "NER" (nonexistent) on Latin text is dropped.
    """

    class _Span:
        def __init__(self, r, source_lang):
            self.start = r.start
            self.end = r.end
            self.entity_type = r.entity_type
            self.score = r.score
            self.source_lang = source_lang

    flat = []
    for idx, rl in enumerate(result_lists):
        for r in rl:
            flat.append(_Span(r, idx))

    # Filter cross-language NER false positives
    NER_TYPES = {"PERSON", "LOCATION", "ORGANIZATION", "DATE_TIME", "NRP"}
    filtered = []
    for s in flat:
        span_text = full_text[s.start:s.end]
        is_ner = s.entity_type in NER_TYPES
        if is_ner:
            if s.source_lang in (0, 1) and _has_arabic(span_text) and not _has_latin(span_text):
                continue
        filtered.append(s)

    # Sort: earliest start, longest span first
    filtered.sort(key=lambda s: (s.start, -s.end, -s.score))

    merged = []
    for s in filtered:
        if not merged:
            merged.append(s)
            continue
        top = merged[-1]
        if s.start >= top.end:
            merged.append(s)
        elif s.entity_type == top.entity_type:
            # Same entity type → keep the longer, more complete span
            if (s.end - s.start) > (top.end - top.start):
                merged[-1] = s
        elif s.score > top.score:
            merged[-1] = s

    return merged


_DEFAULT_MULTI_LANG = ("fr", "ar")


def anonymize(text_input, language=None):
    """
    Analyse *text_input* for PII entities, then anonymise them in-place.

    For Algerian documents (which commonly mix Arabic and French), the
    analyzer is run against both ``"fr"`` and ``"ar"`` and results are
    merged, keeping the highest-scoring entity when spans overlap.

    Parameters
    ----------
    text_input : str
        Raw document text to process.
    language : str or None, optional
        ISO 639-1 language code (``"en"``, ``"fr"``, ``"ar"``).
        If ``None`` (default), runs against both ``"fr"`` and ``"ar"``
        and merges results.

    Returns
    -------
    str or AnonymizerResult
        If entities were found and processed, returns an ``AnonymizerResult``
        with a ``.text`` attribute. If nothing was found, returns the
        original string unchanged.
    """
    _ensure_engines()

    if language is None:
        langs = _DEFAULT_MULTI_LANG
    else:
        langs = (language,)

    all_results = []
    for lang in langs:
        results = run_analyzer(_analyzer, text_input, language=lang)
        all_results.append(results)

    merged = _merge_results(*all_results, full_text=text_input)

    if not merged:
        return text_input

    from presidio_analyzer import RecognizerResult
    restored = [
        RecognizerResult(r.entity_type, r.start, r.end, r.score)
        for r in merged
    ]

    operators = _build_operators()
    anonymized_text = anonymize_with_pseudonyms(text_input, restored, operators)

    from collections import namedtuple
    AnonymizerResult = namedtuple("AnonymizerResult", ["text"])
    return AnonymizerResult(text=anonymized_text)


def anonymize_file(path, language=None):
    raw_text, metadata = read_file(path)
    result = anonymize(raw_text, language=language)
    return result, metadata
