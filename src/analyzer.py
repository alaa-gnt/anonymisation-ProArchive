from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import StanzaNlpEngine, NlpEngineProvider

from src.recognizers import (
    DZPhoneRecognizer,
    DZNINRecognizer,
    DZPassportRecognizer,
    DZRIbRecognizer,
    DZIbanRecognizer,
    DZRcRecognizer,
    DZNifRecognizer,
    DZNisRecognizer,
    DZPostalRecognizer,
    DZGlinerRecognizer,
)

# default Presidio recognizers that are not relevant for Algerian context and should be removed
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
    recognizers = []
    for lang in _LANGUAGES:
        recognizers.append(DZPhoneRecognizer(supported_language=lang))
        recognizers.append(DZNINRecognizer(supported_language=lang))
        recognizers.append(DZPassportRecognizer(supported_language=lang))
        recognizers.append(DZRIbRecognizer(supported_language=lang))
        recognizers.append(DZIbanRecognizer(supported_language=lang))
        recognizers.append(DZRcRecognizer(supported_language=lang))
        recognizers.append(DZNifRecognizer(supported_language=lang))
        recognizers.append(DZNisRecognizer(supported_language=lang))
        recognizers.append(DZPostalRecognizer(supported_language=lang))

        recognizers.append(
            PatternRecognizer(
                supported_entity="LOCATION",
                deny_list=_WILAYA_NAMES,
                supported_language=lang,
            )
        )
        recognizers.append(
            PatternRecognizer(
                supported_entity="PERSON",
                deny_list=_ARABIC_FIRST_NAMES,
                supported_language=lang,
            )
        )

        recognizers.append(DZGlinerRecognizer(supported_language=lang))
    return recognizers


def _build_nlp_engine():
    models = [
        {"lang_code": "en", "model_name": "en"},
        {"lang_code": "fr", "model_name": "fr"},
        {"lang_code": "ar", "model_name": "ar"},
    ]
    return StanzaNlpEngine(models=models, download_if_missing=False)


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


_shared_analyzer = None


def get_analyzer():
    global _shared_analyzer
    if _shared_analyzer is None:
        _shared_analyzer = setup_compliance_analyzer()
    return _shared_analyzer


def run_analyzer(analyzer_engine, text_input, language="en"):
    results = analyzer_engine.analyze(
        text=text_input,
        language=language,
    )
    return results
