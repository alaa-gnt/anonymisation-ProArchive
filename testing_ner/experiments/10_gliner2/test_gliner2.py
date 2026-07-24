"""
Experiment 10: GLiNER2 (fastino-ai)
Usage: python test_gliner2.py [file_path]
"""

import sys, time, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evaluation.metrics import ner_precision_recall_f1

RESULTS_DIR = Path("results/10_gliner2")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

print("Loading GLiNER2...")
try:
    from gliner2 import GLiNER2
    model = GLiNER2.from_pretrained("fastino-ai/Gliner2-v1")
    has_gliner2 = True
except Exception as e:
    print(f"  Could not load GLiNER2: {e}")
    print("  Falling back to original GLiNER.")
    has_gliner2 = False

if not has_gliner2:
    from gliner import GLiNER
    model = GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")

LABELS = ["person", "phone number", "email", "location", "date",
          "medical condition", "organization", "company", "national id number"]

TEST_DOCS = {
    "French Contract": {"text": "Monsieur Mehdi Benali, né le 15 mars 1990 à Alger, email: mehdi@company.dz, téléphone: 0551234567.", "ground_truth": []},
    "English Medical": {"text": "Patient John Smith was diagnosed with Diabetes by Dr. Sarah Johnson at Mount Sinai Hospital in New York on 2023-05-12.", "ground_truth": []},
    "Arabic Identity": {"text": "الاسم الكامل: يوسف بن موسى، تاريخ الميلاد: 15/03/1990، رقم الهاتف: 0551234567، الجزائر.", "ground_truth": []},
}

if len(sys.argv) > 1:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8").strip()
    TEST_DOCS = {path.name: {"text": text, "ground_truth": []}}

all_results = []
for doc_name, doc in TEST_DOCS.items():
    print(f"\n{'='*60}\n  Document: {doc_name}\n{'='*60}")
    start = time.time()
    predictions = model.predict_entities(doc["text"], LABELS, threshold=0.5)
    elapsed = time.time() - start
    entities = [{"text": e["text"], "type": e["label"]} for e in predictions]
    for e in entities:
        print(f"  {e['text']:30s} → {e['type']:20s}")
    print(f"\n  Time: {elapsed:.3f}s  |  Entities: {len(entities)}")
    all_results.append({"document": doc_name, "time_sec": round(elapsed, 3), "entities_found": entities})

with open(RESULTS_DIR / "gliner2_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\nResults -> {RESULTS_DIR / 'gliner2_results.json'}")
