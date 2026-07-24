"""
Experiment 7: CamemBERT-NER (French)
Usage: python test_camembert.py [file_path]
"""

import sys, time, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evaluation.metrics import ner_precision_recall_f1

RESULTS_DIR = Path("results/07_camembert")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
from transformers import pipeline

print("Loading CamemBERT-NER (Jean-Baptiste/camembert-ner)...")
ner_pipe = pipeline("token-classification", model="Jean-Baptiste/camembert-ner", aggregation_strategy="simple")
print("Done.\n")

TEST_DOCS = {
    "French Contract": {"text": "Monsieur Mehdi Benali, né le 15 mars 1990 à Alger, email: mehdi@company.dz, téléphone: 0551234567.", "ground_truth": []},
    "French Company": {"text": "La société SPA Digital Services, représentée par son gérant Monsieur Karim Hadj, a signé un contrat de 5 000 000 DZD.", "ground_truth": []},
}

if len(sys.argv) > 1:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8").strip()
    TEST_DOCS = {path.name: {"text": text, "ground_truth": []}}

all_results = []
for doc_name, doc in TEST_DOCS.items():
    print(f"\n{'='*60}\n  Document: {doc_name}\n{'='*60}")
    start = time.time()
    predictions = ner_pipe(doc["text"])
    elapsed = time.time() - start
    entities = [{"text": e["word"], "type": e["entity_group"], "start": e["start"], "end": e["end"]} for e in predictions]
    for e in entities:
        print(f"  {e['text']:30s} → {e['type']:15s}  [{e['start']}:{e['end']}]")
    print(f"\n  Time: {elapsed:.3f}s  |  Entities: {len(entities)}")
    all_results.append({"document": doc_name, "time_sec": round(elapsed, 3), "entities_found": entities})

with open(RESULTS_DIR / "camembert_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\nResults -> {RESULTS_DIR / 'camembert_results.json'}")
