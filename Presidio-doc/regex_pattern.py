from presidio_analyzer import Pattern , PatternRecognizer

# defining the regex pattern (custom pattern) to be recognized
# the score is how much presidio should be trusted this result comparing to other recognition methods
number_pattern = Pattern(name="number_pattern", regex=r"\d+" , score=0.5)

#define recognizer with one or more patterns 
number_recognizer = PatternRecognizer(
    supported_entity="NUMBER", patterns=[number_pattern]
)


text2 = "I live in 510 Broad st."
numbers_result = number_recognizer.analyze(text=text2, entities=["NUMBER"])

print("Result:")
print(numbers_result)
