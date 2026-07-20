from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider


# Country-specific and noisy recognizers that cause false positives
# on Algerian documents (US SSN hitting random ID numbers, etc.)
_TO_REMOVE = {
    "UsBankRecognizer",
    "UsLicenseRecognizer",
    "UsItinRecognizer",
    "UsPassportRecognizer",
    "UsSsnRecognizer",
    "NhsRecognizer",
    "CryptoRecognizer",
    "MedicalLicenseRecognizer",
    "MacAddressRecognizer",
}


# Algerian wilaya names in French, English, and Arabic transliteration.
# Covers official spellings found in government documents.
_WILAYA_NAMES = [
    # 01-10
    "Adrar",
    "Chlef", "Chellif",
    "Laghouat",
    "Oum El Bouaghi", "Oum el Bouaghi",
    "Batna",
    "Béjaïa", "Bejaia",
    "Biskra",
    "Béchar", "Bechar",
    "Blida",
    "Bouira",
    # 11-20
    "Tamanrasset", "Tamanghasset",
    "Tébessa", "Tebessa",
    "Tlemcen",
    "Tiaret",
    "Tizi Ouzou",
    "Alger", "Algiers",
    "Djelfa",
    "Jijel", "Djijel",
    "Sétif", "Setif",
    "Saïda", "Saida",
    # 21-30
    "Skikda",
    "Sidi Bel Abbès", "Sidi Bel Abbes",
    "Annaba",
    "Guelma",
    "Constantine",
    "Médéa", "Medea",
    "Mostaganem",
    "M'Sila", "Msila",
    "Mascara",
    "Ouargla",
    # 31-40
    "Oran",
    "El Bayadh",
    "Illizi",
    "Bordj Bou Arréridj", "Bordj Bou Arreridj",
    "Boumerdès", "Boumerdes",
    "El Tarf",
    "Tindouf",
    "Tissemsilt",
    "El Oued",
    "Khenchela",
    # 41-50
    "Souk Ahras",
    "Tipaza",
    "Mila",
    "Aïn Defla", "Ain Defla",
    "Naâma", "Naama",
    "Aïn Témouchent", "Ain Temouchent",
    "Ghardaïa", "Ghardaia",
    "Relizane",
    "Timimoun",
    "Bordj Badji Mokhtar",
    # 51-58
    "Ouled Djellal",
    "Béni Abbès", "Beni Abbes",
    "In Salah",
    "In Guezzam",
    "Touggourt",
    "Djanet",
    "El Meghaïer", "El Meghaier", "El M'Ghair",
    "El Menia",
]


_LANGUAGES = ["en", "fr"]


def _make_dz_recognizers():
    """Build custom Algerian entity recognizers for all supported languages."""
    lang_configs = [
        {
            "supported_entity": "DZ_PHONE",
            "patterns": [Pattern(name="dz_mobile", regex=r"\b(05|06|07)\d{8}\b", score=0.95)],
        },
        {
            "supported_entity": "DZ_NIN",
            "patterns": [Pattern(name="dz_nin", regex=r"\b\d{6}\s?\d{6}\s?\d{6}\b", score=0.95)],
        },
        {
            "supported_entity": "DZ_PASSPORT",
            "patterns": [Pattern(name="dz_passport", regex=r"\b[A-Z]{2}\d{6}\b", score=0.95)],
        },
        {
            "supported_entity": "DZ_RIB",
            "patterns": [Pattern(name="dz_rib", regex=r"\b\d{20}\b", score=0.95)],
        },
        {
            "supported_entity": "DZ_RC",
            "patterns": [Pattern(name="dz_rc", regex=r"\b[A-Z]{1,2}\d{7,10}\b", score=0.95)],
        },
        {
            "supported_entity": "DZ_NIF",
            "patterns": [Pattern(name="dz_nif", regex=r"\b\d{15}\b", score=0.95)],
        },
        {
            "supported_entity": "DZ_WILAYA",
            "patterns": [Pattern(name="dz_wilaya", regex=r"\b(0[1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-8]|5[0-8])\b", score=0.3)],
        },
        {
            "supported_entity": "DZ_POSTAL",
            "patterns": [Pattern(name="dz_postal", regex=r"\b(0[1-9]|1[0-9]|2[0-9]|3[0-9]|4[0-8]|5[0-8])\d{3}\b", score=0.85)],
        },
        {
            "supported_entity": "DZ_SSN",
            "patterns": [Pattern(name="dz_ssn", regex=r"\b[12]\d{12,14}\b", score=0.95)],
        },
        {
            "supported_entity": "LOCATION",
            "deny_list": _WILAYA_NAMES,
        },
    ]

    recognizers = []
    for lang in _LANGUAGES:
        for cfg in lang_configs:
            kwargs = {"supported_language": lang}
            recognizers.append(PatternRecognizer(**cfg, **kwargs))
    return recognizers


def _build_nlp_engine():
    """Create a multi-language NLP engine supporting English and French."""
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            {"lang_code": "en", "model_name": "en_core_web_lg"},
            {"lang_code": "fr", "model_name": "fr_core_news_md"},
        ],
    }
    provider = NlpEngineProvider(nlp_configuration=configuration)
    return provider.create_engine()


def setup_compliance_analyzer():
    nlp_engine = _build_nlp_engine()

    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine,
        supported_languages=["en", "fr"],
    )

    # Strip out recognizers that are irrelevant or cause false positives
    recognizers_to_keep = [
        r
        for r in analyzer.registry.recognizers
        if r.__class__.__name__ not in _TO_REMOVE
    ]
    analyzer.registry.recognizers = recognizers_to_keep

    # Register all custom Algerian recognizers
    for recognizer in _make_dz_recognizers():
        analyzer.registry.add_recognizer(recognizer)

    return analyzer


def run_analyzer(analyzer_engine, text_input, language="en"):
    results = analyzer_engine.analyze(
        text=text_input,
        language=language,
    )
    return results
