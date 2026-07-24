# Testing NER — NER Model Comparison for PII Detection

Compare Stanza, spaCy, Flair, and GLiNER on French / Arabic / English documents.

## Structure

```
testing_ner/
├── experiments/01_stanza/         → Stanza NER
├── experiments/02_spacy/          → spaCy NER
├── experiments/03_flair/          → Flair NER
├── experiments/04_gliner/         → GLiNER zero-shot NER
├── experiments/05_comparison/     → Compare all together
├── benchmark/NER/                 → Test documents with PII
├── datasets/                      → Real documents by domain
├── evaluation/metrics.py          → Precision / Recall / F1
├── results/                       → Output goes here
└── docs/Architecture/             → Write conclusions here
```

## How to Run

```powershell
# 1. Install
pip install -r requirements.txt
python -m spacy download en_core_web_lg
python -m spacy download fr_core_news_md

# 2. Test one model
python experiments/01_stanza/test_stanza.py

# 3. Compare all
python experiments/05_comparison/compare_all.py
```

## What Each Script Measures

- Entities detected (type, text, position)
- Detection speed
- Precision / Recall / F1 (if ground truth available)
- Behaviour on French vs Arabic vs English
