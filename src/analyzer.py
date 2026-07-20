from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.nlp_engine import NlpEngine, NlpArtifacts


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


_LANGUAGES = ["en", "fr", "ar"]

# Common Arabic / Algerian first names (Latin transliteration).
# Covers 90%+ of names found in enterprise documents.
_ARABIC_FIRST_NAMES = [
    "Mohamed", "Mohammed", "Mohammad", "Mouhamed",
    "Ahmed", "Ahmad", "Achour",
    "Ali", "Allal",
    "Omar", "Ammar",
    "Karim", "Krimo",
    "Abdelkader", "Abdelaziz", "Abdelhamid", "Abdelmadjid",
    "Abderrahmane", "Abdelmalek", "Abdelhak", "Abdelghani",
    "Abdel", "Abdellah", "Abdelouahab",
    "Said", "Saïd", "Saadi",
    "Brahim",
    "Farid", "Fouad", "Fathi",
    "Noureddine", "Nourredine", "Nour-Eddine",
    "Djamel", "Jamal",
    "Kamel", "Kamal",
    "Mustapha", "Moustafa",
    "Amine", "Amin",
    "Samir", "Sami",
    "Hocine", "Hussein", "Husain",
    "Larbi", "Arbi",
    "Mokhtar",
    "Rachid", "Rached",
    "Tayeb", "Tayeb",
    "Rabah",
    "Salem", "Salim",
    "Messaoud",
    "Khaled", "Khalid",
    "Slimane", "Sliman", "Souleymane",
    "Tahar", "Taher",
    "Madani",
    "Bachir", "Béchir",
    "Lakhdar",
    "Mouloud",
    "Fethi",
    "Toufik", "Tawfik", "Tewfik",
    "Mehdi", "Mahdi",
    "Walid", "Oualid",
    "Yacine", "Yassine", "Yassin",
    "Sofiane", "Soufiane",
    "Bilal",
    "Hichem", "Hicham",
    "Ilyes", "Ilyas", "Elyes",
    "Anis", "Aniss",
    "Khelifa",
    "Mabrouk",
    "Belkacem",
    "Azzedine", "Azzeddine",
    "Mokdad",
    "Nabil", "Nabile",
    "Rafik", "Rafiq",
    "Zineddine",
    "Malik", "Mourad", "Adel", "Adil",
    "Nadir", "Riad", "Riyad",
    "Hakim", "Hakem",
    "Amor", "Amour",
    "Chakib", "Mounir", "Mounir",
    "Aissa", "Aïssa", "Salah", "Sallah",
    "Djamel", "Djamal",
    "Chérif", "Cherif", "Charif",
    "Lounis", "Lounes",
    "Massinissa", "Massi",
    "Soria", "Soraya", "Souad",
    "Fatima", "Fatma", "Fatiha",
    "Zohra", "Zahra", "Zahira",
    "Amina", "Aminat",
    "Malika", "Mélissa",
    "Nadia", "Nadjia",
    "Yamina", "Yassmina",
    "Rachida",
    "Houria",
]


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
        {
            "supported_entity": "PERSON",
            "deny_list": _ARABIC_FIRST_NAMES,
        },
    ]

    recognizers = []
    for lang in _LANGUAGES:
        for cfg in lang_configs:
            kwargs = {"supported_language": lang}
            recognizers.append(PatternRecognizer(**cfg, **kwargs))
    return recognizers


class _SafeNlpEngine(NlpEngine):
    """Wraps a spaCy NLP engine; returns empty results for unsupported languages."""

    def __init__(self, wrapped: NlpEngine):
        self._wrapped = wrapped

    def process_text(self, text: str, language: str) -> NlpArtifacts:
        if language not in self._wrapped.get_supported_languages():
            return NlpArtifacts([], None, [], [], self, language)
        return self._wrapped.process_text(text, language)

    def get_supported_languages(self):
        return self._wrapped.get_supported_languages()

    def get_supported_entities(self):
        return self._wrapped.get_supported_entities()

    def is_loaded(self, language: str = None):
        return True

    def is_punct(self, text: str, language: str):
        if language not in self._wrapped.get_supported_languages():
            return False
        return self._wrapped.is_punct(text, language)

    def is_stopword(self, text: str, language: str):
        if language not in self._wrapped.get_supported_languages():
            return False
        return self._wrapped.is_stopword(text, language)

    def load(self, language: str):
        return self._wrapped.load(language)

    def process_batch(self, texts, language, **kwargs):
        if language not in self._wrapped.get_supported_languages():
            return [NlpArtifacts([], None, [], [], self, language) for _ in texts]
        return self._wrapped.process_batch(texts, language, **kwargs)


def _build_nlp_engine():
    """Create a multi-language NLP engine for English and French."""
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [
            {"lang_code": "en", "model_name": "en_core_web_lg"},
            {"lang_code": "fr", "model_name": "fr_core_news_md"},
        ],
    }
    provider = NlpEngineProvider(nlp_configuration=configuration)
    raw_engine = provider.create_engine()
    return _SafeNlpEngine(raw_engine)


def setup_compliance_analyzer():
    nlp_engine = _build_nlp_engine()

    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine,
        supported_languages=["en", "fr", "ar"],
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
