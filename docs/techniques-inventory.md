# Analyzer Engine — Techniques Inventory

## Neural / ML Models

| Technique | What | Used For | File |
|-----------|------|----------|------|
| **Stanza NER** (Stanford) | Neural NER pipeline, 3 models: `en`, `fr`, `ar` | PERSON, ORG, LOC, GPE, DATE, MONEY, etc. | `src/analyzer.py:208-213` |
| **GLiNER** (zero-shot NER) | Model `urchade/gliner_multi_pii-v1`, threshold `0.35` | DZ_NIN, DZ_PASSPORT, DZ_PHONE, EMAIL, IBAN, DZ_RIB | `src/recognizers/dz_gliner.py` |
| **PyTorch** | DL framework to run GLiNER | Backend for GLiNER | `docs/requirements.txt` |

---

## Regex-Based Recognizers (Custom Algerian)

| Recognizer | Entity | Pattern / Method | Score | File |
|-----------|--------|-----------------|-------|------|
| DZPhoneRecognizer | `DZ_PHONE` | mobile `(05\|06\|07)\d{8}` + landline `0(2\|3\|4)\d{7,8}` | 0.95 | `src/recognizers/dz_phone.py` |
| DZNINRecognizer | `DZ_NIN` | 18 digits (6-6-6 format) + **Luhn checksum** validation | 0.95 | `src/recognizers/dz_id_card.py` |
| DZPassportRecognizer | `DZ_PASSPORT` | old `[A-Z]{2}\d{6}` (0.95) + new `\d{9}` with **context boosting** ±50 chars (0.95 w/ context, 0.30 w/o) | 0.30–0.95 | `src/recognizers/dz_passport.py` |
| DZRIbRecognizer | `DZ_RIB` | 20 digits + **mod-97 checksum** | 0.95 | `src/recognizers/dz_rib.py` |
| DZIbanRecognizer | `IBAN_CODE` | `DZ\d{22}` + **mod-97 IBAN validation** | 0.95 | `src/recognizers/dz_iban.py` |
| DZRcRecognizer | `DZ_RC` | `YY / WW - XXXXXX` with **wilaya code validation** (01–58) | 0.95 | `src/recognizers/dz_rc.py` |
| DZNifRecognizer | `DZ_NIF` | 15 digits | 0.95 | `src/recognizers/dz_nif.py` |
| DZNisRecognizer | `DZ_NIS` | 15 digits | 0.95 | `src/recognizers/dz_nis.py` |
| DZPostalRecognizer | `DZ_POSTAL` | 5 digits with **wilaya prefix validation** (01–58) | 0.85 | `src/recognizers/dz_postal.py` |

---

## Deny-List Recognizers

| List | Entity | Entries | Defined In |
|------|--------|---------|------------|
| **Wilaya names** | `LOCATION` | 58 wilayas × spelling variants (~96 entries) | `src/analyzer.py:188-194` |
| **Arabic first names** | `PERSON` | ~140 common names + variants | `src/analyzer.py:195-201` |

---

## Presidio Built-in Recognizers

**Kept:** Email, Phone, CreditCard, Url, Domain, Ip, Age, Numeric + Stanza-powered Person, Location, Organization, DateTime.

**Stripped** (9 removed at `src/analyzer.py:225-230`):
UsBank, UsLicense, UsItin, UsPassport, UsSsn, Nhs, Crypto, MedicalLicense, MacAddress.

---

## Validation / Checksum Algorithms

| Algorithm | Used By | File |
|-----------|---------|------|
| **Luhn (mod-10)** | DZ_NIN validation | `src/recognizers/_checksums.py:13-18` |
| **mod-97 (ISO 7064)** | DZ_RIB validation | `src/recognizers/_checksums.py:21-32` |
| **mod-97 + IBAN rearrange** | IBAN_CODE validation | `src/recognizers/_checksums.py:35-45` |

---

## Pipeline Orchestration

| Technique | Detail | File |
|-----------|--------|------|
| **Multi-language scan** | Runs analyzer on all 3 langs (`en`, `fr`, `ar`) sequentially | `src/pipeline.py:78-86` |
| **Cross-language FP filter** | Discards NER results from en/fr that contain only Arabic chars (Unicode range 0x0600–0x06FF) | `src/pipeline.py:38-47` |
| **Span merging heuristics** | Overlap resolution: same type → keep longest; different type → keep highest score | `src/pipeline.py:49-67` |
| **Pseudonymization** | Custom (not Presidio's): groups by normalized value, sequential `<ENTITY_N>` tags; PERSON normalized to first word only | `src/anonymizer.py` |
