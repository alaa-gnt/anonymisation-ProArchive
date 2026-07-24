"""
Experiment 12: DzNER-Based Models (Algerian Arabic NER)
Tests models from the DzNER paper + practical alternatives for Algerian NER.

NOTE: The DzNER GitHub repo (Dahouabdelhalim/NER-model-on-the-DzNER-corpus)
contains Jupyter notebooks that FINE-TUNE existing models (AraBERT, MARBERT,
ARBERT, DziriBERT, mBERT) on the DzNER dataset. No pre-trained weights are
available — you must train them yourself using the notebooks.

This script tests:
  1. The base models used in the DzNER paper
  2. An alternative already-trained Algerian NER model from HuggingFace
"""

import sys, time, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evaluation.metrics import ner_precision_recall_f1

RESULTS_DIR = Path("results/12_dzner_models")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

# ============================================================
#  1. TEST DOCUMENTS (Algerian Arabic)
# ============================================================
TEST_DOCS = {
    "Algerian Identity (Arabic)": {
        "text": "الاسم الكامل: يوسف بن موسى، تاريخ الميلاد: 15/03/1990، "
                "رقم الهاتف: 0551234567، الجزائر.",
        "ground_truth": [
            {"text": "يوسف بن موسى", "type": "PER", "start": 15, "end": 27},
            {"text": "الجزائر", "type": "LOC", "start": 70, "end": 76},
        ]
    },
    "Algerian Company (Arabic)": {
        "text": "شركة سوناطراك للنفط والgas في الجزائر. مديرها هو السيد توفيق.",
        "ground_truth": [
            {"text": "سوناطراك", "type": "ORG", "start": 9, "end": 18},
            {"text": "الجزائر", "type": "LOC", "start": 33, "end": 39},
            {"text": "توفيق", "type": "PER", "start": 56, "end": 62},
        ]
    },
}

# ============================================================
#  2. MODELS TO TEST
# ============================================================

# --- Option A: CAMeLBERT-NER (already tested in exp09, but best Arabic NER available) ---
# We include it here for comparison with the DzNER-based approaches

# --- Option B: algerianDeBERTa (real estate NER, but handles Algerian dialect well) ---
def test_algerian_deberta(text):
    """Test a practical Algerian NER model from HuggingFace."""
    model_name = "81melody/algerianDeBERTa-realestate-ner-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    nlp = pipeline("token-classification", model=model, tokenizer=tokenizer,
                    aggregation_strategy="simple")
    return nlp(text)

# --- Option C: Base DziriBERT (not fine-tuned for NER, but shows the base model's capabilities) ---
def test_dziribert_base(text):
    """DziriBERT as used in DzNER paper — note: no NER head."""
    tokenizer = AutoTokenizer.from_pretrained("alger-ia/dziribert")
    tokens = tokenizer.tokenize(text)
    return tokens  # Just tokenization, no NER

# ============================================================
#  3. RUN
# ============================================================
all_results = []

print("=" * 60)
print("  DzNER-Based Models — Algerian Arabic NER")
print("=" * 60)

print("\n--- Testing: 81melody/algerianDeBERTa-realestate-ner-v2 ---")
for doc_name, doc in TEST_DOCS.items():
    print(f"\n  Document: {doc_name}")
    print(f"  Text: {doc['text'][:60]}...")

    try:
        start = time.time()
        predictions = test_algerian_deberta(doc["text"])
        elapsed = time.time() - start

        entities = [{"text": e["word"], "type": e["entity_group"],
                      "start": e["start"], "end": e["end"]}
                    for e in predictions]

        for e in entities:
            print(f"    {e['text']:30s} → {e['type']:20s}")

        metrics = ner_precision_recall_f1(doc["ground_truth"], entities)
        print(f"  Time: {elapsed:.3f}s  |  F1: {metrics['f1']:.2%}")

        all_results.append({
            "model": "algerianDeBERTa-ner",
            "document": doc_name,
            "time_sec": round(elapsed, 3),
            "entities_found": entities,
            "metrics": metrics,
        })
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n--- Notes on DzNER models from the paper ---")
print("""
The DzNER paper (Dahou et al., 2023) fine-tunes these base models on the DzNER dataset:
  - AraBERT v02         (aubmindlab/bert-base-arabertv02)
  - MARBERT             (UBC-NLP/MARBERT)
  - ARBERT              (UBC-NLP/ARBERT)
  - DziriBERT           (alger-ia/dziribert)
  - mBERT               (bert-base-multilingual-cased)

To reproduce: run the notebooks at:
  https://github.com/Dahouabdelhalim/NER-model-on-the-DzNER-corpus/tree/main/Models

Alternatively, test the base models on your documents using experiment 09
(CAMeLBERT) which already has an Arabic NER head available.
""")

with open(RESULTS_DIR / "dzner_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print(f"\nResults -> {RESULTS_DIR / 'dzner_results.json'}")
