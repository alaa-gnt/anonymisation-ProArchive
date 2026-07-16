from presidio_analyzer import PatternRecognizer, AnalyzerEngine

# defining a custom list of titles to be recognized
titles_list = [
    "Sir",
    "Ma'am",
    "Madam",
    "Mr.",
    "Mrs.",
    "Ms.",
    "Miss",
    "Dr.",
    "Professor",
]

# building the recognizer for that speacific list 
titles_recognizer = PatternRecognizer(
    supported_entity="TITLE",
    deny_list=titles_list
)

text1 = "I suspect Professor Plum, in the Dining Room, with the candlestick"

#the anlyzing engine 
analyzer = AnalyzerEngine()

# adding the cu
analyzer.registry.add_recognizer(titles_recognizer)

results = analyzer.analyze(
    text=text1,
    language="en"
)

for r in results:
    print(
        text1[r.start:r.end],
        "->",
        r.entity_type
    )