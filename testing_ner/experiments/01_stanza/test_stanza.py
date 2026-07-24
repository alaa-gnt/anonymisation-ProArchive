"""
Experiment 1: Stanza NER
Usage: python test_stanza.py [file_path]
"""

import sys, time, json, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evaluation.metrics import ner_precision_recall_f1

RESULTS_DIR = Path("results/01_stanza")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
import stanza

def detect_lang(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return "ar"
    if re.search(r'[a-zA-Z]', text):
        if any(w in text.lower() for w in ["le", "la", "les", "des", "est", "dans", "monsieur", "madame", "né"]):
            return "fr"
        return "en"
    return "fr"

TEST_DOCS = {
    "French Contract": {"lang": "fr", "text": "Monsieur Mehdi Benali, né le 15 mars 1990 à Alger, email: mehdi@company.dz, téléphone: 0551234567.", "ground_truth": []},
    "English Medical": {"lang": "en", "text": "Patient John Smith was diagnosed with Diabetes by Dr. Sarah Johnson at Mount Sinai Hospital in New York on 2023-05-12.", "ground_truth": []},
    "Arabic Identity": {"lang": "ar", "text": "الاسم الكامل: يوسف بن موسى، تاريخ الميلاد: 15/03/1990، رقم الهاتف: 0551234567، الجزائر.", "ground_truth": []},
}

if len(sys.argv) > 1:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8").strip()
    lang = detect_lang(text)
    print(f"  Auto-detected language: {lang}")
    TEST_DOCS = {path.name: {"lang": lang, "text": text, "ground_truth": []}}

print("Loading Stanza models...")
pipelines = {}
for lang in set(d["lang"] for d in TEST_DOCS.values()):
    print(f"  Loading {lang}...")
    pipelines[lang] = stanza.Pipeline(lang, processors="tokenize,ner", verbose=False, download_method=stanza.DownloadMethod.REUSE_RESOURCES)
print("Done.\n")

all_results = []
for doc_name, doc in TEST_DOCS.items():
    print(f"\n{'='*60}\n  Document: {doc_name}  ({doc['lang']})\n{'='*60}")
    nlp = pipelines[doc["lang"]]
    start = time.time()
    processed = nlp(doc["text"])
    elapsed = time.time() - start
    entities = [{"text": ent.text, "type": ent.type, "start": ent.start_char, "end": ent.end_char} for ent in processed.ents]
    for e in entities:
        print(f"  {e['text']:30s} → {e['type']:15s}  [{e['start']}:{e['end']}]")
    print(f"\n  Time: {elapsed:.3f}s  |  Entities: {len(entities)}")
    all_results.append({"document": doc_name, "language": doc["lang"], "time_sec": round(elapsed, 3), "entities_found": entities})

with open(RESULTS_DIR / "stanza_results.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\nResults -> {RESULTS_DIR / 'stanza_results.json'}")
