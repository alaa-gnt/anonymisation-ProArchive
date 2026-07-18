# Anonymisation-ProArchive — System Architecture

## Overview

This document describes the complete architecture of the PII anonymisation Proof-of-Concept built on top of Microsoft Presidio. The system acts as a **privacy-preserving middleware** positioned between enterprise documents and cloud-based LLMs.

The core principle: **sensitive data is detected and neutralised locally before any payload reaches external AI services.**

---

## 1. Architectural Diagram

```
                     ┌──────────────────────┐
                     │    Input Document     │
                     │  (PDF / TXT / DOCX    │
                     │   / Scanned Image)    │
                     └──────────┬───────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────┐
│          1. DOCUMENT INGESTION LAYER              │
│                                                   │
│   ┌──────────────┐  ┌──────────────────────┐     │
│   │ File Reader  │  │ Text Extractor       │     │
│   │  - PDF (pdfplumber / PyMuPDF)          │     │
│   │  - DOCX (python-docx)                  │     │
│   │  - Images (Tesseract OCR)             │     │
│   │  - Plain text               │  Encoding       │
│   └──────────────┘               Detection       │
│                                  (UTF-8 /         │
│                                   Latin-1 /       │
│                                   Arabic W1256)   │
│                                  └────────────────┘
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│          2. LANGUAGE DETECTION & ROUTING          │
│                                                   │
│   ┌──────────────────────────┐                    │
│   │ Language Detector        │                    │
│   │ (langdetect / fastText)  │                    │
│   └───────────┬──────────────┘                    │
│               │                                   │
│        ┌──────┼──────┐                            │
│        ▼             ▼              ▼             │
│   ┌─────────┐ ┌──────────┐ ┌──────────┐          │
│   │ English │ │ French   │ │ Arabic   │          │
│   │ Pipeline│ │ Pipeline │ │ Pipeline │          │
│   └─────────┘ └──────────┘ └──────────┘          │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│          3. PII DETECTION ENGINE                  │
│                                                   │
│   ┌─────────────────────────────────────────┐    │
│   │          AnalyzerEngine (Presidio)       │    │
│   │                                          │    │
│   │  ┌────────────┐  ┌──────────────────┐   │    │
│   │  │ NLP Engine │  │  Recognizer      │   │    │
│   │  │ (spaCy)    │  │  Registry        │   │    │
│   │  │            │  │                  │   │    │
│   │  │ en_core_web│  │  ┌─────────────┐ │   │    │
│   │  │ _lg        │  │  │ Built-in    │ │   │    │
│   │  │            │  │  │ Recognizers │ │   │    │
│   │  │ fr_core_   │  │  │ (PERSON,    │ │   │    │
│   │  │ news_md    │  │  │  EMAIL, ...)│ │   │    │
│   │  │            │  │  └─────────────┘ │   │    │
│   │  │ Arabic:    │  │  ┌─────────────┐ │   │    │
│   │  │ custom     │  │  │ Custom DZ   │ │   │    │
│   │  │ tokenizer  │  │  │ Recognizers │ │   │    │
│   │  │ + Camel-   │  │  │             │ │   │    │
│   │  │ liger NER  │  │  │ DZ_PHONE    │ │   │    │
│   │  └────────────┘  │  │ DZ_ID_CARD  │ │   │    │
│   │                  │  │ DZ_PASSPORT │ │   │    │
│   │                  │  │ FR_SECU_SOC │ │   │    │
│   │                  │  │ FR_SIRET    │ │   │    │
│   │                  │  │ AR_NATIONAL │ │   │    │
│   │                  │  │ _ID         │ │   │    │
│   │                  │  │ CUSTOM_RULES│ │   │    │
│   │                  │  └─────────────┘ │   │    │
│   └─────────────────────────────────────────┘    │
│                                                   │
│   Detection Methods:                              │
│   ┌──────────┬─────────────┬──────────────────┐  │
│   │ Method   │ Description │ Example          │  │
│   ├──────────┼─────────────┼──────────────────┤  │
│   │ NLP NER  │ spaCy model │ "Mehdi"→PERSON   │  │
│   │ Regex    │ Pattern     │ \b05\d{8}→PHONE  │  │
│   │ Deny List│ Exact match │ "Dr."→TITLE      │  │
│   │ Custom   │ Python      │ EMP-12345→       │  │
│   │ Logic    │ function    │ EMPLOYEE_ID      │  │
│   └──────────┴─────────────┴──────────────────┘  │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│          4. RISK CLASSIFIER (Legal Layer)         │
│                                                   │
│   Maps each detected entity to a legal category   │
│   defined in legal_baseline.tex (Loi 18-07/25-11) │
│                                                   │
│   ┌──────────────┬──────────────────┬──────────┐ │
│   │ Category     │ Examples         │ Action   │ │
│   ├──────────────┼──────────────────┼──────────┤ │
│   │ I: Direct    │ PERSON, EMAIL,   │ Mandatory│ │
│   │ Identifiers  │ PHONE, ID_NUMBER │ removal  │ │
│   ├──────────────┼──────────────────┼──────────┤ │
│   │ II: Quasi-   │ BIRTH_DATE,      │ k-anony- │ │
│   │ Identifiers  │ POSTAL_CODE,     │ mity     │ │
│   │              │ JOB_TITLE        │ check    │ │
│   ├──────────────┼──────────────────┼──────────┤ │
│   │ III: Sensi-  │ HEALTH, RELIGION,│ Absolute │ │
│   │ tive Data    │ POLITICS, GENETIC│ BLOCK    │ │
│   └──────────────┴──────────────────┴──────────┘ │
│                                                   │
│   If Category III detected → document REJECTED    │
│   (Article 18 compliance — absolute prohibition)  │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│          5. ANONYMISATION ENGINE                  │
│                                                   │
│   ┌─────────────────────────────────────────┐    │
│   │       AnonymizerEngine (Presidio)        │    │
│   │                                          │    │
│   │  Receives: text + analyzer_results       │    │
│   │  + operator map                          │    │
│   │                                          │    │
│   │  Entity → Operator → Config              │    │
│   │  ┌──────────┬───────────┬─────────────┐  │    │
│   │  │ PERSON   │ replace   │ <ALGERIAN_  │  │    │
│   │  │          │           │ CITIZEN>    │  │    │
│   │  ├──────────┼───────────┼─────────────┤  │    │
│   │  │ EMAIL    │ hash      │ SHA-256     │  │    │
│   │  ├──────────┼───────────┼─────────────┤  │    │
│   │  │ PHONE    │ mask      │ ******789   │  │    │
│   │  ├──────────┼───────────┼─────────────┤  │    │
│   │  │ ID_CARD  │ replace   │ <REDACTED>  │  │    │
│   │  ├──────────┼───────────┼─────────────┤  │    │
│   │  │ BIRTH    │ generalize│ 1990→1990s  │  │    │
│   │  │ _DATE    │           │             │  │    │
│   │  └──────────┴───────────┴─────────────┘  │    │
│   └─────────────────────────────────────────┘    │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│          6. POST-PROCESSING & AUDIT               │
│                                                   │
│   ┌─────────────────────┐  ┌──────────────────┐  │
│   │ Text Reconstruction │  │ Audit Log        │  │
│   │  - Merge spans      │  │ (Article 38      │  │
│   │  - Preserve format  │  │  compliance)     │  │
│   │  - Restore line     │  │                  │  │
│   │    breaks           │  │  Timestamp       │  │
│   │                     │  │  Doc hash        │  │
│   │                     │  │  Entities found  │  │
│   │                     │  │  Actions taken   │  │
│   │                     │  │  Operator name   │  │
│   └─────────────────────┘  └──────────────────┘  │
└──────────────────────┬───────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────┐
│          7. OUTPUT LAYER                          │
│                                                   │
│   ┌──────────────┐  ┌────────────────────┐       │
│   │ Sanitised    │  │ Metadata JSON      │       │
│   │ Text         │  │  - original spans  │       │
│   │              │  │  - replacements    │       │
│   │  → cloud LLM │  │  - risk category   │       │
│   │              │  │  - language        │       │
│   │              │  │                    │       │
│   │              │  │  → local storage   │       │
│   │              │  │    (not sent to    │       │
│   │              │  │     cloud)         │       │
│   └──────────────┘  └────────────────────┘       │
└──────────────────────────────────────────────────┘
```

---

## 2. Detection Methods (Layer 3 Detail)

### 2.1 NLP Model (spaCy NER)

| Language | Model | Entities Covered |
|----------|-------|-----------------|
| English | `en_core_web_lg` | PERSON, ORG, GPE, DATE, MONEY, etc. |
| French | `fr_core_news_md` | PER, ORG, LOC, DATE, MONEY, etc. |
| Arabic | Custom (Camel-lliger / Farasa) | PER, ORG, LOC (limited coverage) |

### 2.2 Regex Patterns

| Entity | Pattern | Language |
|--------|---------|----------|
| DZ_PHONE | `\b(05\|06\|07)\d{8}\b` | DZ |
| DZ_ID_CARD | `\b\d{1,2}\s?\d{4}\s?\d{4}\b` (Algerian ID format) | DZ |
| DZ_PASSPORT | `\b[A-Z]{2}\d{6}\b` | DZ |
| FR_PHONE | `\b(0[1-9])(\s?\d{2}){4}\b` | FR |
| FR_SECU_SOC | `\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b` | FR |
| FR_SIRET | `\b\d{14}\b` | FR |
| EMAIL | Built-in Presidio recognizer | All |
| CREDIT_CARD | Built-in Presidio recognizer | All |

### 2.3 Deny List Recognizers

Lists of known titles, departments, roles, and sensitive keywords per language.

### 2.4 Custom Rule-Based Recognizers

Extends `EntityRecognizer` to implement business-specific logic, e.g.:
- "EMP-" prefix followed by 5 digits → EMPLOYEE_ID (unless followed by "temporary")
- Context-based detection ("Dr." before a name → PERSON with higher confidence)

---

## 3. Anonymisation Strategies (Layer 5 Detail)

| Operator | Effect | Use Case | Example |
|----------|--------|----------|---------|
| `replace` | Substitute with placeholder text | Names, IDs | `Mehdi Benali` → `<ALGERIAN_CITIZEN>` |
| `hash` | Irreversible SHA-256 hash | Emails (for session linking) | `mehdi@x.com` → `a3f2b...` |
| `mask` | Partially replace characters | Phone numbers | `0551234567` → `******4567` |
| `redact` | Full removal (replace with empty) | Unnecessary PII | — |
| `generalize` | Replace with broader category | Age → range, Date → year only | `1990-05-12` → `1990` |

### Strategy Decision Matrix

Based on the legal category (from `legal_baseline.tex`):

| Category | Allowed Operators | Notes |
|----------|------------------|-------|
| I: Direct Identifiers | `replace`, `hash`, `redact` | Must be fully non-recoverable |
| II: Quasi-Identifiers | `mask`, `generalize` | Must satisfy k-anonymity (k ≥ 5) |
| III: Sensitive Data | `block` (reject document) | Article 18 absolute prohibition |

---

## 4. Data Flow (Sequence)

```
User                  Pipeline                 Cloud LLM
 │                       │                        │
 │  Upload document      │                        │
 │──────────────────────>│                        │
 │                       │                        │
 │                  ┌────┴────┐                   │
 │                  │1. Ingest│                   │
 │                  │2. Detect│                   │
 │                  │   Lang  │                   │
 │                  └────┬────┘                   │
 │                       │                        │
 │                  ┌────┴────┐                   │
 │                  │3. Analyze│                  │
 │                  │   (PII) │                   │
 │                  └────┬────┘                   │
 │                       │                        │
 │                  ┌────┴────┐                   │
 │                  │4. Classify│                 │
 │                  │   Risk   │                  │
 │                  └────┬────┘                   │
 │                       │                        │
 │                  ┌────┴────┐                   │
 │                  │5. Anonym-│                  │
 │                  │   ise    │                  │
 │                  └────┬────┘                   │
 │                       │                        │
 │                  ┌────┴────┐                   │
 │                  │6. Audit  │                  │
 │                  │   Log    │                  │
 │                  └────┬────┘                   │
 │                       │                        │
 │                  Sanitised text                │
 │                       │───────────────────────>│
 │                       │                        │
 │                       │    LLM Response        │
 │                       │<───────────────────────│
 │                       │                        │
 │  Response to user     │                        │
 │<──────────────────────│                        │
```

---

## 5. Module Inventory & Status

| Module | File | Status | Description |
|--------|------|--------|-------------|
| Analyzer | `analyzer_model.py` | ✅ Complete | Presidio analyzer with DZ_PHONE custom recognizer |
| Anonymizer | `anonymizer_module.py` | ✅ Complete | Presidio anonymizer with replace/hash/mask strategies |
| Pipeline orchestrator | *not yet built* | 🔜 | End-to-end script tying ingestion → analysis → anonymisation |
| Language detector | *not yet built* | 🔜 | Language detection and NLP engine routing |
| French recognizers | *not yet built* | 🔜 | FR-specific regex patterns + spaCy model |
| Arabic recognizers | *not yet built* | 🔜 | Arabic NLP adapter + regex patterns |
| Risk classifier | *not yet built* | 🔜 | Legal category assignment + k-anonymity check |
| Document ingestion | *not yet built* | 🔜 | PDF/DOCX/Image reader + text extraction |
| Audit logger | *not yet built* | 🔜 | DPO compliance register (Article 38) |
| CLI entry point | *not yet built* | 🔜 | User-facing CLI tool |
| Evaluation framework | *not yet built* | 🔜 | Precision/recall against annotated corpus |
| Test suite | *not yet built* | 🔜 | Unit + integration tests |

---

## 6. Legal Compliance Mapping

Each component maps to requirements from `legal_baseline.tex`:

| Legal Article | Requirement | Implemented By |
|---------------|-------------|---------------|
| Art. 3 (18-07) | Define personal data | Risk classifier (Cat I / II / III) |
| Art. 3 (25-11) | Define pseudonymisation | Anonymizer replace/hash strategies |
| Art. 18 (18-07) | Prohibit sensitive data processing | Risk classifier → block Category III |
| Art. 38 (18-07) | Technical security measures | Edge-based sanitisation before API call |
| Art. 44 (18-07) | Cross-border transfer authorisation | Local anonymisation before cloud transmission |

---

## 7. Deployment Context

```
┌────────────────  Enterprise Network  ─────────────────┐
│                                                         │
│   ┌──────────┐    ┌─────────────┐    ┌────────────┐   │
│   │ Document │───>│ Anonymisation│───>│ Sanitised  │   │
│   │ Store    │    │ Pipeline    │    │ Text       │   │
│   └──────────┘    └─────────────┘    └─────┬──────┘   │
│                                            │          │
└────────────────────────────────────────────┼──────────┘
                                             │
                                             │  HTTPS
                                             ▼
                                      ┌──────────┐
                                      │ Cloud LLM │
                                      │ (GPT-4,   │
                                      │  Claude,  │
                                      │  Gemini)  │
                                      └──────────┘
```

The pipeline runs **entirely on-premises** inside the enterprise network. Only the anonymised (PII-free) text crosses the network boundary to the cloud LLM.
