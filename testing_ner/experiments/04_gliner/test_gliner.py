"""
Experiment 4: GLiNER Zero-Shot NER
Usage: python test_gliner.py [file_path]
"""

import sys, time, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evaluation.metrics import ner_precision_recall_f1

RESULTS_DIR = Path("results/04_gliner")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
from gliner import GLiNER

LABELS = ["person", "phone number", "email address", "national id number",
          "passport number", "bank account number", "iban", "location",
          "date", "medical condition", "tax id", "company", "organization"]
THRESHOLDS = [0.3, 0.5, 0.7]

TEST_DOCS = {
    "French Contract": {"text": "Monsieur Mehdi Benali, né le 15 mars 1990 à Alger, email: mehdi@company.dz, téléphone: 0551234567.", "ground_truth": []},
    "English Medical": {"text": "Patient John Smith was diagnosed with Diabetes by Dr. Sarah Johnson at Mount Sinai Hospital in New York on 2023-05-12.", "ground_truth": []},
    "Arabic Identity": {"text": "الاسم الكامل: يوسف بن موسى، تاريخ الميلاد: 15/03/1990، رقم الهاتف: 0551234567، الجزائر.", "ground_truth": []},
}

if len(sys.argv) > 1:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8").strip()
    TEST_DOCS = {path.name: {"text": text, "ground_truth": []}}

print("Loading GLiNER model...")
model = GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")
print("Done.\n")

all_results = []
for doc_name, doc in TEST_DOCS.items():
    print(f"\n{'='*60}\n  Document: {doc_name}\n{'='*60}")
    for threshold in THRESHOLDS:
        start = time.time()
        predictions = model.predict_entities(doc["text"], LABELS, threshold=threshold)
        elapsed = time.time() - start
        entities = [{"text": e["text"], "type": e["label"], "score": e["score"]} for e in predictions]
        print(f"\n  threshold={threshold}  ({len(entities)} entities, {elapsed:.3f}s)")
        for e in entities:
            print(f"    {e['text']:30s} → {e['type']:20s}  ({e['score']:.2f})")
        all_results.append({"document": doc_name, "threshold": threshold, "time_sec": round(elapsed, 3), "entities_found": entities})

with open(RESULTS_DIR / "gliner_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\nResults -> {RESULTS_DIR / 'gliner_results.json'}")
