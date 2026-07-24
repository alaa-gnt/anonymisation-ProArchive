"""
Experiment 5: Compare all NER models on the same documents.
Runs Stanza, spaCy, Flair, GLiNER and prints a comparison table.
"""

import sys, time, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from evaluation.metrics import ner_precision_recall_f1

RESULTS_DIR = Path("results/05_comparison")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
#  1. SAME TEST DOCUMENTS FOR ALL MODELS
# ============================================================
TEST_DOCS = {
    "French Contract": {
        "lang": "fr",
        "text": "Monsieur Mehdi Benali, né le 15 mars 1990 à Alger, "
                "email: mehdi@company.dz, téléphone: 0551234567.",
        "ground_truth": [
            {"text": "Mehdi Benali", "type": "PERSON", "start": 10, "end": 23},
            {"text": "15 mars 1990", "type": "DATE", "start": 33, "end": 45},
            {"text": "Alger", "type": "LOCATION", "start": 49, "end": 54},
        ]
    },
    "English Medical": {
        "lang": "en",
        "text": "Patient John Smith was diagnosed with Diabetes by Dr. Sarah Johnson "
                "at Mount Sinai Hospital in New York on 2023-05-12.",
        "ground_truth": [
            {"text": "John Smith", "type": "PERSON", "start": 8, "end": 18},
            {"text": "Diabetes", "type": "MEDICAL_CONDITION", "start": 40, "end": 48},
            {"text": "Sarah Johnson", "type": "PERSON", "start": 56, "end": 69},
            {"text": "Mount Sinai Hospital", "type": "ORGANIZATION", "start": 73, "end": 93},
            {"text": "New York", "type": "LOCATION", "start": 97, "end": 105},
            {"text": "2023-05-12", "type": "DATE", "start": 109, "end": 119},
        ]
    },
    "Arabic Identity": {
        "lang": "ar",
        "text": "الاسم الكامل: يوسف بن موسى، تاريخ الميلاد: 15/03/1990، "
                "رقم الهاتف: 0551234567، الجزائر.",
        "ground_truth": [
            {"text": "يوسف بن موسى", "type": "PERSON", "start": 15, "end": 27},
            {"text": "15/03/1990", "type": "DATE", "start": 45, "end": 55},
            {"text": "الجزائر", "type": "LOCATION", "start": 70, "end": 76},
        ]
    },
}

# ============================================================
#  2. NORMALISE ENTITY TYPES FOR FAIR COMPARISON
# ============================================================
TYPE_MAP = {
    "PER": "PERSON", "PER": "PERSON", "PERS": "PERSON",
    "LOC": "LOCATION",
    "ORG": "ORGANIZATION",
    "MISC": "OTHER",
    "DATE": "DATE",
    "MEDICAL_CONDITION": "MEDICAL_CONDITION",
}

def normalise_type(t):
    t = t.upper()
    return TYPE_MAP.get(t, t)

# ============================================================
#  3. RUN ALL MODELS
# ============================================================
all_rows = []

# --- Stanza ---
import stanza
print("Loading Stanza...")
stanza_nlp = {}
for lang in set(d["lang"] for d in TEST_DOCS.values()):
    stanza_nlp[lang] = stanza.Pipeline(lang, processors="tokenize,ner", verbose=False,
                                        download_method=stanza.DownloadMethod.REUSE_RESOURCES)

# --- spaCy ---
import spacy
print("Loading spaCy...")
spacy_en = spacy.load("en_core_web_lg")
spacy_fr = spacy.load("fr_core_news_md")
spacy_nlp = {"en": spacy_en, "fr": spacy_fr}

# --- Flair ---
from flair.models import SequenceTagger
from flair.data import Sentence
print("Loading Flair...")
flair_nlp = {
    "fr": SequenceTagger.load("flair/ner-french"),
    "en": SequenceTagger.load("ner"),
}

# --- GLiNER ---
from gliner import GLiNER
print("Loading GLiNER...")
gliner_model = GLiNER.from_pretrained("urchade/gliner_multi_pii-v1")
gliner_labels = ["person", "phone number", "email", "location", "date",
                 "medical condition", "organization", "company"]

def run_gliner(text):
    predictions = gliner_model.predict_entities(text, gliner_labels, threshold=0.5)
    return [{"text": e["text"], "type": e["label"].upper(), "start": 0, "end": 0}
            for e in predictions]

print("Done.\n")

# ============================================================
#  4. RUN & COLLECT
# ============================================================
results_by_model = {
    "Stanza": {},
    "spaCy": {},
    "Flair": {},
    "GLiNER": {},
}

for doc_name, doc in TEST_DOCS.items():
    print(f"\n{'='*60}")
    print(f"  {doc_name}  ({doc['lang']})")
    print(f"{'='*60}")

    # --- Stanza ---
    start = time.time()
    processed = stanza_nlp[doc["lang"]](doc["text"])
    t = time.time() - start
    ents = [{"text": e.text, "type": normalise_type(e.type), "start": e.start_char, "end": e.end_char}
            for e in processed.ents]
    m = ner_precision_recall_f1(doc["ground_truth"], ents)
    results_by_model["Stanza"][doc_name] = {"entities": ents, "metrics": m, "time": t}
    print(f"  [Stanza]  F1={m['f1']:.2%}  time={t:.3f}s")

    # --- spaCy ---
    if doc["lang"] in spacy_nlp:
        start = time.time()
        processed = spacy_nlp[doc["lang"]](doc["text"])
        t = time.time() - start
        ents = [{"text": e.text, "type": normalise_type(e.label_), "start": e.start_char, "end": e.end_char}
                for e in processed.ents]
        m = ner_precision_recall_f1(doc["ground_truth"], ents)
        results_by_model["spaCy"][doc_name] = {"entities": ents, "metrics": m, "time": t}
        print(f"  [spaCy]   F1={m['f1']:.2%}  time={t:.3f}s")
    else:
        print(f"  [spaCy]   SKIP (no Arabic model)")

    # --- Flair ---
    if doc["lang"] in flair_nlp:
        sentence = Sentence(doc["text"])
        start = time.time()
        flair_nlp[doc["lang"]].predict(sentence)
        t = time.time() - start
        ents = [{"text": e.text, "type": normalise_type(e.tag), "start": e.start_position, "end": e.end_position}
                for e in sentence.get_spans("ner")]
        m = ner_precision_recall_f1(doc["ground_truth"], ents)
        results_by_model["Flair"][doc_name] = {"entities": ents, "metrics": m, "time": t}
        print(f"  [Flair]   F1={m['f1']:.2%}  time={t:.3f}s")
    else:
        print(f"  [Flair]   SKIP (no Arabic model)")

    # --- GLiNER ---
    start = time.time()
    ents = run_gliner(doc["text"])
    t = time.time() - start
    m = ner_precision_recall_f1(doc["ground_truth"], ents)
    results_by_model["GLiNER"][doc_name] = {"entities": ents, "metrics": m, "time": t}
    print(f"  [GLiNER]  F1={m['f1']:.2%}  time={t:.3f}s")

# ============================================================
#  5. PRINT SUMMARY TABLE
# ============================================================
print(f"\n\n{'='*70}")
print(f"  SUMMARY — F1 SCORES")
print(f"{'='*70}")
print(f"  {'Model':12s}  {'French':12s}  {'English':12s}  {'Arabic':12s}  {'Avg Time':10s}")
print(f"  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*10}")

for model_name in ["Stanza", "spaCy", "Flair", "GLiNER"]:
    f1s = []
    times = []
    for doc_name in TEST_DOCS:
        if doc_name in results_by_model[model_name]:
            f1s.append(results_by_model[model_name][doc_name]["metrics"]["f1"])
            times.append(results_by_model[model_name][doc_name]["time"])
    avg_time = sum(times) / len(times) if times else 0
    f1_strs = [f"{f:.2%}" for f in f1s]
    while len(f1_strs) < 3:
        f1_strs.append("N/A")
    print(f"  {model_name:12s}  {f1_strs[0]:12s}  {f1_strs[1]:12s}  {f1_strs[2]:12s}  {avg_time:.3f}s")

with open(RESULTS_DIR / "comparison_summary.json", "w", encoding="utf-8") as f:
    json.dump(results_by_model, f, indent=2, ensure_ascii=False)

print(f"\nFull results -> {RESULTS_DIR / 'comparison_summary.json'}")
