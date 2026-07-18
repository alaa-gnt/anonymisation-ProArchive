from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern


def setup_compliance_analyzer():
    analyzer = AnalyzerEngine()

    algerian_phone_pattern = Pattern(
        name="dz_mobile_pattern",
        regex=r"\b(05|06|07)\d{8}\b",
        score=0.85,
    )

    dz_phone_recognizer = PatternRecognizer(
        supported_entity="DZ_PHONE",
        patterns=[algerian_phone_pattern],
    )

    analyzer.registry.add_recognizer(dz_phone_recognizer)

    return analyzer


def run_analyzer(analyzer_engine, text_input):
    target_entities = ["PERSON", "EMAIL_ADDRESS", "DZ_PHONE"]

    results = analyzer_engine.analyze(
        text=text_input,
        language="en",
        entities=target_entities,
    )
    return results