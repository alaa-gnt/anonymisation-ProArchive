"""
Experiment 8: DziriBERT (Algerian Arabic)
BERT pretrained on Algerian Darija — test if it detects named entities.
Note: DziriBERT is a base model (not fine-tuned for NER).
We test it with a simple classification approach.
"""

import sys, time, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

RESULTS_DIR = Path("results/08_dziribert")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

print("Loading DziriBERT...")
try:
    tokenizer = AutoTokenizer.from_pretrained("alger-ia/dziribert")
    model = AutoModelForTokenClassification.from_pretrained("alger-ia/dziribert")
    nlp = pipeline("token-classification", model=model, tokenizer=tokenizer,
                    aggregation_strategy="simple")
    has_ner = True
except Exception:
    print("  DziriBERT does not have a NER head — testing as language model only.")
    has_ner = False

TEST_TEXTS = [
    "الاسم الكامل: يوسف بن موسى، رقم الهاتف: 0551234567، الجزائر.",
    "شركة سوناطراك تعلن عن منصب عمل في الجزائر العاصمة.",
    "محمد يسكن في وهران ويعمل في بنك الفلاحة.",
]

all_results = []

print(f"\n{'='*60}")
print(f"  Testing DziriBERT on {len(TEST_TEXTS)} Arabic texts")
print(f"{'='*60}")

for i, text in enumerate(TEST_TEXTS):
    print(f"\n  Text {i+1}: {text[:80]}")

    if has_ner:
        start = time.time()
        predictions = nlp(text)
        elapsed = time.time() - start
        print(f"  Time: {elapsed:.3f}s  |  Entities: {len(predictions)}")
        for e in predictions:
            print(f"    {e['word']:30s} → {e['entity_group']:15s}  ({e['score']:.2f})")
    else:
        # Just test tokenization (model loads correctly)
        start = time.time()
        tokens = tokenizer.tokenize(text)
        elapsed = time.time() - start
        print(f"  Time: {elapsed:.3f}s  |  Tokens: {len(tokens)}")
        print(f"  [Note: DziriBERT is a base LM — no NER head available]")

    all_results.append({
        "text": text,
        "has_ner_head": has_ner,
        "time_sec": round(elapsed, 3),
    })

with open(RESULTS_DIR / "dziribert_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print(f"\nResults -> {RESULTS_DIR / 'dziribert_results.json'}")
