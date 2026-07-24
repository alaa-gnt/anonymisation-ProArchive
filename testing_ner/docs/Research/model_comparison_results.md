# NER Model Comparison Results

---

## TEXT 1

| Field | Value |
|-------|-------|
| **ID** | Text 1 |
| **Language** | French |
| **Topic** | Civil Registry (Acte de Naissance) |

**Edge cases:**
- Dates in text ("l'an deux mille douze") vs numeric dates (03/07/1985) — no model handles both
- "Novembre" ambiguous — month name vs part of "avenue du 1er Novembre"
- Long document names merged with content ("ACTE DE NAISSANCERépublique Algérienne...")

### Stanza

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| Saida BENALI → PER | l'an deux mille douze (DATE) | Novembre → LOC (should be street name) |
| Karim BENALI → PER | le quinze du mois de mars (DATE) | Direction de la Santé → LOC (should be ORG) |
| Nadia MEZIANE → PER | 03/07/1985 (DATE) | |
| Saida → LOC | 21/11/1988 (DATE) | |
| Tlemcen → LOC | 20 mars 2012 (DATE) | |
| Oran → LOC | avenue du 1er Novembre (LOC) | |
| Alger → LOC | | |

**Speed:** 1.26s

---

### spaCy

Same as Stanza — same entities found ✅, same dates missed ❌. Novembre → MISC (better than Stanza's LOC). Direction de la Santé → ORG ✅ (correct).

**Speed:** 0.18s (7x faster than Stanza)

---

### Flair

Same + improvements: avenue du 1er Novembre → LOC ✅ (Stanza missed this). Direction de la Santé → ORG ✅ (Stanza said LOC). Still misses all dates ❌.

**Speed:** 1.03s

---

### GLiNER (threshold 0.3)

| Improvement over others ✅ | Still misses ❌ |
|---------------------------|----------------|
| 03/07/1985 → DATE ✅ | République Algérienne Démocratique et Populaire |
| 21/11/1988 → DATE ✅ | dates written in text ("l'an deux mille douze", "le quinze du mois de mars") |
| 20 mars → DATE (partial) ✅ | avenue du 1er Novembre (LOC) |
| Direction de la Santé → ORG ✅ | |
| Ministère → ORG ✅ | |

Only model that detected any dates at all. At threshold 0.5 → loses dates but keeps clean entities.

**Speed:** 0.64–1.70s

---

### BERT-NER (dslim/bert-base-NER)

**Terrible.** English-only model on French text → subword fragmentation:
- "##cratique", "##W", "##ila", "Ka", "T", "Or" — broken tokens everywhere
- Most entities are garbage (fragments, not real words)
- Not usable for French/Arabic documents

**Speed:** 0.47s

---

### CamemBERT

| Good ✅ | Bad ❌ / Wrong ⚠️ |
|---------|-------------------|
| avenue du 1er Novembre → LOC ✅ | All dates missed ❌ |
| PERSON names correct ✅ | "Officier de l" → ORG, "État" → ORG, "Civil" → LOC ⚠️ (fragmented, should be one) |
| Locations mostly correct ✅ | "Direction de la Santé" → LOC ⚠️ (should be ORG) |
| | "République Algérienne...Wilaya de Saida" merged as one LOC ⚠️ |

**Speed:** 0.38s

---

### CAMeLBERT

**Terrible on French text.** Arabic-only model on French → subword fragmentation:
- "Algé", "##rien", "##émoc", "##rat", "P", "##opul" — broken fragments
- "##W", "##ilaya" → PERS (garbage)
- "K", "##arim BENALI" → PERS (fragmented name)
- "Tlemce" → PERS (should be LOC, wrong type + incomplete)
- Not usable for French documents

**Speed:** 0.56s

---

### GLiNER2 (threshold 0.5)

| Found ✅ | Missed ❌ |
|---------|----------|
| PERSON: Saida BENALI, Karim BENALI, Nadia MEZIANE ✅ | All dates ❌ |
| LOC: Tlemcen, Oran ✅ | Saida (LOC) ❌ |
| ORG: Direction de la Santé, Ministère, commune de Saida ✅ | Alger (LOC) ❌ |
| Clean — no false positives | avenue du 1er Novembre ❌ |
| | République Algérienne... ❌ |

Fewer entities than GLiNER at 0.3, but higher confidence / less noise.

**Speed:** 0.80s

---

### Summary & Full Picture — Text 1

| Model | PERSON | LOCATION | DATE | ORG | Wrong / Noise | Speed | Verdict |
|-------|---------|----------|------|-----|---------------|-------|---------|
| **Stanza** | ✅ | ✅ (missed avenue 1er Nov) | ❌ all | ⚠️ Direction Santé → LOC | Novembre → LOC | 1.26s | Good baseline |
| **spaCy** | ✅ | ✅ | ❌ all | ✅ Direction Santé → ORG | Minimal | **0.18s** | **Best speed/accuracy balance** |
| **Flair** | ✅ | ✅ (found avenue 1er Nov) | ❌ all | ✅ Direction Santé → ORG | Minor span issues | 1.03s | Good coverage |
| **GLiNER** @0.3 | ✅ | ⚠️ missed avenue 1er Nov | ✅ numeric dates | ✅ | Some noise at 0.3 | 0.64-1.70s | **Only one that finds dates** |
| **GLiNER2** @0.5 | ✅ | ⚠️ missed Saida, Alger | ❌ all | ✅ | Clean | 0.80s | Cleanest, but misses more |
| **BERT-NER** | ❌ fragments | ❌ fragments | ❌ | ❌ | **High** — subword garbage | 0.47s | **Not usable for FR/AR** |
| **CamemBERT** | ✅ | ✅ (found avenue 1er Nov) | ❌ all | ⚠️ fragmented | Some span issues | 0.38s | Good for French |
| **CAMeLBERT** | ❌ fragments | ❌ fragments | ❌ | ❌ | **High** — subword garbage | 0.56s | **Not usable for French** |

**Key Takeaways for Text 1:**
1. **spaCy** is the fastest (0.18s) and most reliable for PERSON/LOC/ORG detection
2. **GLiNER** is the ONLY model that detects numeric dates (03/07/1985, 21/11/1988)
3. **No model** detects dates written in text ("l'an deux mille douze")
4. **Stanza, spaCy, Flair** all give similar results — spaCy is 7x faster
5. **CamemBERT** is good for French but not better than spaCy
6. **BERT-NER and CAMeLBERT** produce garbage on out-of-language documents

---

## TEXT 3

| Field | Value |
|-------|-------|
| **ID** | Text 3 |
| **Language** | French |
| **Topic** | University registration form (short fields, no sentence context) |

**Edge cases:**
- Same word "Saida" used as PERSON surname (Nom field) and LOC birthplace — only distinguishable by field label context
- Short-field key:value format — no sentence context for any NER model
- ID number (118542039871) looks like a number, not a word — only pattern-based models find it
- Phone number (0555 12 34 56) with spaces — only GLiNER2 detects it
- Date (05/09/2001) in a short field — all models miss it
- Field labels phoned, Adresse) look like LOC/ORG to NER models

### Stanza

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| Cité 500 Logements → LOC ✅ | Saida → PERSON (Nom field) ❌ merged with "Prénom" | "Saida \nPrénom" → ORG ⚠️ |
| | Karim → PER ❌ merged with "Date" | "Karim\nDate" → PER (merged) ⚠️ |
| | 05/09/2001 → DATE ❌ | "Saida\nWilaya" → LOC (merged) ⚠️ |
| | 118542039871 → ID ❌ completely missed | "Saida\nAdresse" → LOC (merged) ⚠️ |
| | Téléphone → completely missed | Université Dr. Moulay Tahar → LOC ❌ (should be ORG) |
| | | "Saida\nFilière...N° Carte Nationale" → MISC (merged everything) ⚠️ |
| | | "Téléphone" → MISC (just a field label) ❌ |

**Speed:** 0.11s

**Verdict:** Struggles with short-field format — merges field labels with values, misses the ID number, can't distinguish Saida as PERSON vs LOC without sentence context.

---

### spaCy

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| Université Dr. Moulay Tahar → ORG ✅ | 05/09/2001 → DATE ❌ (merged with label) | "Saida \nPrénom" → PER (merged, but Saida is PER here ✅ — correct type) |
| | 118542039871 → ID ❌ | "Karim\nDate de naissance" → PER (merged) ⚠️ |
| | Téléphone number ❌ | "05/09/2001\nLieu" → PER (wrong type + merged) ❌ |
| | | "Saida\nWilaya" → PER ❌ (should be LOC) |
| | | "Saida\nAdresse" → PER ❌ (should be LOC) |
| | | "N°", "Carte Nationale" → ORG (field label fragments) ❌ |
| | | "FICHE", "INSCRIPTION" → MISC (labels) ❌ |
| | | "Téléphone" → LOC ❌ (label) |

**Speed:** 0.04s (fastest)

**Verdict:** Very fast but same short-field problem as Stanza — merges values with labels, misses ID and phone.

---

### Flair

Same issue — short-field format confuses all models. Université → ORG ✅. Everything else merged with labels.

| Correct ✅ | Wrong/Merged ⚠️ |
|-----------|-----------------|
| Université Dr. Moulay Tahar → ORG ✅ | "Saida \nPrénom" → PER (merged) |
| | "Karim\nDate" → PER (merged) |
| | "Saida\nWilaya" → PER (merged, should be LOC) |
| | "Saida\nAdresse : Cité 500 Logements" → PER (merged with address) |
| | "Informatique N°" → MISC (field fragment) |
| | "Carte Nationale" → ORG (label fragment) |
| | "Téléphone" → LOC (label) |

**Speed:** 0.02s

**Verdict:** Same as Stanza/spaCy — form fields break the sentence-based NER approach.

---

### GLiNER (threshold 0.3)

Same short-field problem. Merged everything into large MISC spans.

| Found ⚠️ | Missed ❌ |
|----------|---------|
| "FICHE D'INSCRIPTION...Date de naissance" → MISC (merged everything) | All individual PER, LOC, DATE, ID ❌ |
| "Lieu de naissance...Cité 500 Logements" → MISC (merged) | |
| "Saida Établissement" → LOC | |
| Université Dr. Moulay Tahar → LOC ❌ (should be ORG) | |
| "Informatique N°...Téléphone" → MISC (merged with ID) | |

**Speed:** 0.50s

**Verdict:** Same problem — form fields don't provide sentence context for NER.

---

### BERT-NER (dslim/bert-base-NER)

Heavy subword fragmentation on form fields. Worse than previous texts.

**Speed:** 1.54s

**Verdict:** Not usable for form text.

---

### CamemBERT

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|---------|
| **Saida → PER ✅** (standalone, not merged — first model to do this) | 05/09/2001 → DATE ❌ | Saida Wilaya → LOC (merged with Wilaya) ⚠️ |
| **Karim → PER ✅** (standalone — first model) | 118542039871 → ID ❌ | Université → LOC ❌ (should be ORG) |
| Saida → LOC ✅ (multiple, standalone) | Téléphone ❌ | Carte Nationale → LOC ❌ (should be ORG) |
| Cité 500 Logements → LOC ✅ | | |

**Best performer on Text 3 so far** — only model that successfully separated "Saida" as PERSON vs LOC without merging with field labels.

**Speed:** 0.93s

---

### CAMeLBERT

Heavy subword fragmentation on French text. Not usable.

**Speed:** 0.13s

---

### GLiNER2 (threshold 0.5)

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| **118542039871 → national id number ✅** (only model to detect this!) | Saida (Nom field) → location ❌ (should be PERSON) |
| **0555 12 34 56 → phone number ✅** (only model to detect this!) | |
| Karim → person ✅ | |
| Saida → location ✅ (birthplace + Wilaya) | |
| Université → organization ✅ | |

**Only model that detected the ID number and phone number** — because it uses pattern matching, not sentence context.

**Speed:** 0.53s

---

### Summary & Full Picture — Text 3

| Model | PERSON | LOCATION | ORG | DATE | ID / PHONE | Labels merged? | Speed | Verdict |
|-------|---------|----------|-----|------|-----------|----------------|-------|---------|
| **Stanza** | ❌ merged | ❌ merged | ❌ | ❌ | ❌ | **Yes** | 0.11s | Form fields break it |
| **spaCy** | ⚠️ merged | ⚠️ merged | ✅ Uni | ❌ | ❌ | **Yes** | **0.04s** | Too fast, too merged |
| **Flair** | ⚠️ merged | ⚠️ merged | ✅ Uni | ❌ | ❌ | **Yes** | 0.02s | Same problem |
| **GLiNER** @0.3 | ❌ all in one MISC | ❌ | ❌ | ❌ | ❌ | **Yes** (chunked) | 0.50s | Worst on form fields |
| **GLiNER2** @0.5 | ⚠️ Saida→LOC wrong | ✅ 2x Saida LOC | ✅ Uni | ❌ | **✅ ID + Phone** | Partial | 0.53s | **Only one that finds ID/phone** |
| **BERT-NER** | ❌ fragments | ❌ fragments | ❌ | ❌ | ❌ | Fragments | 1.54s | Not usable |
| **CamemBERT** | ✅ **Saida + Karim standalone** | ✅ 3x Saida LOC | ❌ Uni→LOC | ❌ | ❌ | **Minimal** | 0.93s | **Best on PERSON/LOC separation** |
| **CAMeLBERT** | ❌ fragments | ❌ fragments | ❌ | ❌ | ❌ | Fragments | 0.13s | Not usable on French |

**Key Takeaways for Text 3 (short-field form):**
1. **CamemBERT** handles short fields best — only model that separates PERSON vs LOC "Saida" without merging
2. **GLiNER2** is the only model that finds ID numbers and phone numbers (pattern-based detection)
3. **No model** detects dates in form fields (05/09/2001)
4. **All traditional NER models** merge field labels with values — the short-field format is a fundamental weakness
5. **Conclusion for your project**: Form-based documents need a **different approach** — regex + field label mapping, not just NER

---

## TEXT 2

| Field | Value |
|-------|-------|
| **ID** | Text 2 |
| **Language** | French + Arabic (bilingual) |
| **Topic** | Court document (TRIBUNAL DE ORAN) |

**Edge cases:**
- French + Arabic mixed in same document — only GLiNER/GliNER2 handle both
- Arabic text layout is right-to-left but embedded in left-to-right document
- Same person named in both French (Yacine SAIDANI) and Arabic (يسين سعيداني)
- Hijri + Gregorian date paired as single entity (12 Rajab 1443 / 14/02/2022)
- ORG names span both languages (Société NAFTAL / شركة نفطال)
- "Rajab" ambiguous — month name (DATE) vs possible PER

### Stanza

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| يسين سعيداني → PER | NAFTAL (ORG) | TRIBUNAL DE ORAN → MISC (should be ORG) |
| البليدة → LOC | شركة نفطال (ORG) | Yacine SAIDANI → MISC merged with other text (should be PER) |
| سيدي بلعباس → LOC | Sonatrach (ORG) | Farouk BOUZID → MISC merged with other text (should be PER) |
| | commune de Saida (LOC) | |
| | 12 Rajab 1443 (DATE) | |
| | 14/02/2022 (DATE) | |
| | Blida (LOC) | |

**Speed:** 0.45s

---

### spaCy

| French part | Arabic part |
|------------|-------------|
| Yacine SAIDANI → PER ✅ | ❌ all Arabic text completely ignored |
| Blida → LOC ✅ | |
| Société NAFTAL → ORG ✅ | |
| Sonatrach → ORG ✅ | |
| Saida → LOC ✅ | |
| TRIBUNAL DE ORAN → MISC ⚠️ (should be ORG) | |
| Monsieur → PER (partial — missed Farouk BOUZID) ❌ | |
| Rajab → LOC ❌ (should be DATE) | |

As expected — spaCy doesn't handle Arabic at all.

**Speed:** 0.18s

---

### Flair

| Found ✅ | Wrong ⚠️ | Missed ❌ |
|---------|----------|---------|
| Yacine SAIDANI → PER ✅ | TRIBUNAL → MISC (should be ORG) | All Arabic text ❌ |
| ORAN → LOC ✅ | Chambre CivileAffaire → LOC (should be ORG) | Farouk BOUZID surname ❌ |
| Blida → LOC ✅ | Rajab → PER (should be DATE) | 12 Rajab 1443 / 14/02/2022 ❌ |
| Société NAFTAL → ORG ✅ | | شركة نفطال, سيدي بلعباس, etc. ❌ |
| Sonatrach → ORG ✅ | | |
| Saida → LOC ✅ | | |
| Monsieur Farouk → PER (partial) ⚠️ | | |

**Speed:** 1.03s

---

### GLiNER (threshold 0.3)

| Found ✅ | Wrong ⚠️ | Missed ❌ |
|---------|----------|---------|
| Yacine SAIDANI → person ✅ | TRIBUNAL DE ORAN → company (should be ORG) | 14/02/2022 as separate date (merged with Hijri) |
| Farouk BOUZID → person ✅ | شركة نفطالمسؤولة → merged with next word | |
| يسين سعيداني → person ✅ | | |
| Blida → location ✅ | | |
| البليدة → location ✅ | | |
| سيدي بلعباس → location ✅ | | |
| Société NAFTAL → company ✅ | | |
| Sonatrach → company ✅ | | |
| commune de Saida → location ✅ | | |
| 12 Rajab 1443 (14/02/2022 → date ✅ | | |

Best model so far for Text 2 — found almost everything.

**Speed:** 0.29–0.59s

---

### BERT-NER (dslim/bert-base-NER)

| Slightly better ⚠️ | Still bad ❌ |
|-------------------|-------------|
| TRIBUNAL DE ORAN → ORG ✅ (first model to get this right) | Heavy subword fragmentation |
| Société NAF → ORG (partial) | "##AN", "##U", "##ID" → ORG (garbage) |
| Saida → LOC ✅ | "B" → LOC (fragment of Blida) |
| | "Son" → LOC (fragment of Sonatrach, wrong type) |
| | All Arabic text completely ignored |
| | Most names are fragments (Yacine SA, Farouk) |

Slightly better than Text 1 on French ORG detection, but still unusable due to fragmentation.

**Speed:** 0.47s

---

### CamemBERT

| Found ✅ | Wrong ⚠️ | Missed ❌ |
|---------|----------|---------|
| Yacine SAIDANI → PER ✅ | TRIBUNAL DE ORAN → LOC (should be ORG) | All Arabic text ❌ |
| Farouk BOUZID → PER ✅ (full name — better than spaCy/Flair) | Chambre Civile → LOC (should be ORG) | All dates ❌ |
| Blida → LOC ✅ | Rajab → MISC (should be DATE) | commune de Saida ❌ |
| Société NAFTAL → ORG ✅ | | |
| Sonatrach → ORG ✅ | | |
| Saida → LOC ✅ | | |

**Speed:** 1.50s

---

### CAMeLBERT

| Arabic part | French part |
|------------|-------------|
| سيدي بلعباس → LOC ✅ | Ch, ##ambre C → PERS (garbage) ❌ |
| البلي + ##دة → LOC (fragmented) ⚠️ | Monsieur Y → PERS (partial) ❌ |
| يسي + ##ن سعيداني → PERS (fragmented) ⚠️ | Soci → LOC (garbage) ❌ |
| | Monsieur Farouk BO → PERS (partial) ❌ |
| | Saida → PERS (should be LOC) ❌ |
| | ##onatra → LOC (part of Sonatrach, wrong) ❌ |

Same problem as Text 1 — struggles with French text, Arabic is fragmented but partially usable.

**Speed:** 0.22s

---

### GLiNER2 (threshold 0.5)

| Found ✅ | Missed ❌ |
|---------|----------|
| TRIBUNAL DE ORAN → organization ✅ (GLiNER said company) | commune de Saida (LOC) ❌ |
| Yacine SAIDANI → person ✅ | |
| Farouk BOUZID → person ✅ | |
| يسين سعيداني → person ✅ | |
| Blida → location ✅ | |
| البليدة → location ✅ | |
| سيدي بلعباس → location ✅ | |
| Société NAFTAL → company ✅ | |
| Sonatrach → company ✅ | |
| 12 Rajab 1443 (14/02/2022 → date ✅ | |

All entity types correct. Only missed commune de Saida compared to GLiNER at 0.3.

**Speed:** 0.80s

---

### Summary & Full Picture — Text 2

| Model | PERSON | LOCATION | ORG | DATE | Arabic text | Speed | Verdict |
|-------|---------|----------|-----|------|-------------|-------|---------|
| **Stanza** | Arabic PER ✅, French PER ⚠️ merged + MISC | Arabic LOC ✅, French LOC partial ⚠️ | ❌ all missed | ❌ | Partial | 0.45s | Arabic OK, French ORG/DATE weak |
| **spaCy** | French PER ✅ | French LOC ✅ | French ORG ✅ | ❌ | ❌ ignored | **0.18s** | French only, best speed |
| **Flair** | French PER partial ⚠️ | French LOC ✅ | French ORG ✅ | ❌ | ❌ ignored | 1.03s | French only, similar to spaCy |
| **GLiNER** @0.3 | ✅ all PER (FR+AR) | ✅ all LOC (FR+AR) | ✅ almost all ORG | ✅ **12 Rajab 1443 + 14/02/2022** | ✅ full support | 0.29-0.59s | **Best overall — only model that handles everything** |
| **GLiNER2** @0.5 | ✅ all PER (FR+AR) | ⚠️ missed commune de Saida | ✅ all ORG (TRIBUNAL → ORG ✅) | ✅ date | ✅ full support | 0.80s | Cleaner but misses some |
| **BERT-NER** | ⚠️ partial/fragments | ⚠️ fragments | ⚠️ TRIBUNAL → ORG ✅ (only model) | ❌ | ❌ ignored | 0.47s | Fragmented but got 1 thing right |
| **CamemBERT** | ✅ French PER (full names) | ✅ French LOC | ⚠️ TRIBUNAL → LOC (wrong) | ❌ | ❌ ignored | 1.50s | Good French names, wrong ORG |
| **CAMeLBERT** | ⚠️ Arabic PER fragmented | ⚠️ Arabic LOC fragmented | ❌ | ❌ | Partial (fragmented) | 0.22s | Arabic only, fragmented |

**Key Takeaways for Text 2:**
1. **GLiNER at 0.3** is the clear winner — only model that handles both French + Arabic + dates
2. **No traditional NER model** (Stanza, spaCy, Flair, CamemBERT) detects dates or handles bilingual text
3. **spaCy** is best for French-only portions (fast, accurate)
4. **GLiNER2** is cleaner but misses slightly more than GLiNER at 0.3
5. **BERT-NER** accidentally got TRIBUNAL DE ORAN → ORG right — the only model to do so
6. **CAMeLBERT** is too fragmented to be useful even on Arabic

---

## TEXT 5

| Field | Value |
|-------|-------|
| **ID** | Text 5 |
| **Language** | French |
| **Topic** | Business letter (SONELGAZ raccordement) |

**Edge cases:**
- "SAIDI" (surname) vs "Saida" (city) vs "Saida" inside company name "Les Frères Saida Import-Export" — three entity boundaries for the same root word
- "Les Frères Saida Import-Export" must stay as single ORG — should NOT split "Saida" out as separate LOC
- "Wilaya de SaidaMonsieur" — no space between "Saida" and "Monsieur", tests if model correctly tokenizes
- "Amine SAIDI, Tél : +213 661 22 33 44" — name and phone label now properly separated (previously merged as "SAIDITél")
- "08 janvier 2026" — French date in text (not numeric), hard for most models
- "+213 661 22 33 44" — phone number with country code and spaces

### Stanza

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| Agence SONELGAZ → ORG ✅ | 08 janvier 2026 → DATE ❌ | Wilaya de SaidaMonsieur le Directeur → ORG ❌ (merged with address line) |
| **Amine SAIDI ×2 → PER ✅** (both mentions!) | +213 661 22 33 44 → phone ❌ | Tél → LOC ⚠️ (field label detected as entity) |
| Les Frères Saida Import-Export → ORG ✅ **(kept as single span!)** | | |
| Zone Industrielle de Sidi Bel Abbès → LOC ✅ | | |
| Route de Mascara → LOC ✅ | | |
| Saida → LOC ✅ | | |

**Speed:** 0.34s

---

### spaCy

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| **Amine SAIDI ×2 → PER ✅** (both mentions!) | 08 janvier 2026 → DATE ❌ | Agence SONELGAZ → LOC ❌ (should be ORG) |
| Les Frères Saida Import-Export → ORG ✅ | +213 661 22 33 44 → phone ❌ | Wilaya de SaidaMonsieur le Directeur → LOC ❌ (merged) |
| Route de Mascara → LOC ✅ | Wilaya de Saida → LOC ❌ (merged + cut) | **Saida → PER ❌** (should be LOC) |
| Tél → PER ⚠️ (field label) | | **Zone Industrielle** → split from "Sidi Bel Abbès" ⚠️ |

**Speed:** 0.04s (fastest)

---

### Flair

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| Agence SONELGAZ → ORG ✅ | 08 janvier 2026 → DATE ❌ | Directeur,Je soussigné → PER ❌ (garbage) |
| Amine SAIDI → PER ✅ | +213 661 22 33 44 → phone ❌ | **2026.Cordialement,Amine SAIDI → LOC ❌** (second name merged with date+garbage) |
| Frères Saida Import-Export → ORG ✅ (missing "Les" only) | Wilaya de Saida → LOC ❌ (cut at "Monsieur") | Tél → MISC |
| Zone Industrielle de Sidi Bel Abbès → LOC ✅ | | |
| Route de Mascara → LOC ✅ | | |
| Saida → LOC ✅ | | |

**Speed:** 0.60s

---

### GLiNER (threshold 0.3 / 0.5 / 0.7)

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| **Amine SAIDI ×2 → person ✅** (both mentions now!) | SONELGAZ ❌ | |
| **Les Frères Saida Import-Export → company ✅ (kept as single span!)** | Wilaya de Saida ❌ | |
| **Zone Industrielle de Sidi Bel Abbès → location ✅** | Route de Mascara ❌ | |
| **08 janvier 2026 → date ✅** (only model!) | Saida (standalone) ❌ | |
| **+213 661 22 33 44 → phone number ✅** (only model!) | | |

**Only model that detects date + phone + both name mentions.** Identical results across all thresholds (all scores ≥ 0.91).

**Speed:** 0.26–1.05s

---

### BERT-NER (dslim/bert-base-NER)

Heavy subword fragmentation. Not usable.

| Wrong ⚠️ / Garbage |
|-------------------|
| "W" → PER, "##ila" → PER, "##ya" → PER (fragments of Wilaya) |
| "Am" → PER, "SA" → PER, "##ID" → ORG (fragments of SAIDI) |
| "Fr" → ORG, "##ères Saida" → MISC (fragments of Frères) |
| "Co" → PER (fragment of Cordialement) |
| 19 entities, mostly garbage fragments |

**Speed:** 1.78s

---

### CamemBERT

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| **SONELGAZ → ORG ✅** (clean, without "Agence") | 08 janvier 2026 → DATE ❌ | Frères Saida Import-Export → ORG ⚠️ (missing "Les") |
| **Wilaya de Saida → LOC ✅** (only model to extract this cleanly despite no space!) | +213 661 22 33 44 → phone ❌ | Tél not detected |
| **Amine SAIDI ×2 → PER ✅** (both mentions — fixed by separating from Tél!) | | |
| Zone Industrielle de Sidi Bel Abbès → LOC ✅ | | |
| Route de Mascara → LOC ✅ | | |
| Saida → LOC ✅ | | |

**Best traditional model for Text 5** — only one to correctly extract "Wilaya de Saida" despite the missing space. Both "Amine SAIDI" mentions now correctly detected.

**Speed:** 1.61s

---

### CAMeLBERT

Complete garbage on French text — 30 entities, mostly fragments. Not usable.

**Speed:** 0.81s

---

### GLiNER2 (fallback to GLiNER — model repo not found)

Same output as GLiNER:

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| **Amine SAIDI ×2 → person ✅** (both mentions!) | |
| Les Frères Saida Import-Export → company ✅ | |
| Zone Industrielle de Sidi Bel Abbès → location ✅ | |
| 08 janvier 2026 → date ✅ | |
| +213 661 22 33 44 → phone number ✅ | |

**Speed:** 0.98s

---

### Summary & Full Picture — Text 5

| Model | PERSON | LOCATION | ORG | DATE | PHONE | "Saida in company" kept as ORG? | Wilaya de Saida extracted? | Speed | Verdict |
|-------|---------|----------|-----|------|-------|-------------------------------|---------------------------|-------|---------|
| **Stanza** | ✅ **×2 name mentions** | ✅ (missed Wilaya) | ✅ | ❌ | ❌ | **✅** | ❌ merged | 0.34s | Good ORG span, both names found |
| **spaCy** | ✅ **×2 name mentions** | ⚠️ split ZI, Saida→PER | ⚠️ SONELGAZ→LOC | ❌ | ❌ | ✅ (but includes noise) | ❌ merged | **0.04s** | Fast, both names, low quality |
| **Flair** | ⚠️ first name OK, second merged with date | ✅ (cut Wilaya) | ✅ (missing "Les") | ❌ | ❌ | ✅ but missing "Les" | ❌ cut | 0.60s | Second name still broken |
| **GLiNER** | ✅ **×2 name mentions** | ❌ missed several | ❌ missed SONELGAZ | **✅** | **✅** | **✅** | ❌ missed | 0.26-1.05s | **Only one with date+phone+both names** |
| **GLiNER2** | ✅ **×2 name mentions** | ❌ missed several | ❌ missed SONELGAZ | **✅** | **✅** | **✅** | ❌ missed | 0.98s | Same as GLiNER (fallback) |
| **BERT-NER** | ❌ fragments | ❌ fragments | ❌ fragments | ❌ | ❌ | ❌ fragments | ❌ fragments | 1.62s | Not usable |
| **CamemBERT** | ✅ **×2 name mentions** | **✅ Wilaya de Saida clean!** | **✅ SONELGAZ clean** | ❌ | ❌ | ⚠️ missing "Les" | **✅ (only model!)** | 1.61s | **Best on LOC/ORG + both names** |
| **CAMeLBERT** | ❌ fragments | ❌ fragments | ❌ fragments | ❌ | ❌ | ❌ fragments | ❌ fragments | 0.40s | Not usable on French |

**Key Takeaways for Text 5 (Business Letter):**
1. **GLiNER** is the only model that detects **date + phone** — pattern-based detection beats context for these
2. **CamemBERT** is best for clean LOC/ORG extraction — only model that correctly extracts "Wilaya de Saida" despite no space after "Saida"
3. **"Les Frères Saida Import-Export"** kept as single ORG by most models (Stanza, GLiNER, GLiNER2) ✅ — no model incorrectly split "Saida" as separate LOC
4. **No traditional model** (Stanza, spaCy, Flair, CamemBERT) detects the date or phone
5. **Fixing "SAIDITél" → "SAIDI, Tél"** unlocked correct double name detection in all models except Flair. **GLiNER** is the only model that gets: date + phone + both name mentions + company ORG intact in a single pass.

---

## TEXT 6

| Field | Value |
|-------|-------|
| **ID** | Text 6 |
| **Language** | French |
| **Topic** | Contract (mixed calendar, IDs, money) |

**Edge cases:**
- **Hijri date in text** ("27 Chaabane 1446") — easy to misclassify as MISC or LOC
- **Hijri + Gregorian paired** ("27 Chaabane 1446 correspondant au 26/02/2025")
- **CNI numbers** (095384721, 118273645) — purely numeric, must NOT be tagged as date or phone
- **"SAIDI" surname vs "Saida" city** — same word, different entity types
- **"350 000 DA"** — currency amount with spaces, no model has a MONEY label
- **"CPA"** — 3-letter bank acronym, easy to miss
- **"Saida" ×2** — one standalone, one in "agence CPA de Saida"

### Stanza

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| Béjaïa → LOC ✅ | 27 Chaabane 1446 → DATE ❌ | **27 Chaabane → LOC ❌** (Hijri date misclassified) |
| Saida → LOC ✅ (standalone) | 26/02/2025 → DATE ❌ | entreMme Warda HAMDI → ORG ❌ (merged with "entreMme") |
| CPA de Saida → ORG ✅ | 095384721 → CNI ❌ | CNI → ORG ⚠️ (just the label, not the number) |
| | Nabil SAIDI → PER ✅ (partial, with "M.") | |
| | 118273645 → CNI ❌ | |
| | 350 000 DA → MONEY ❌ | |
| | 01/03/2025 → DATE ❌ | |

**Speed:** 0.53s

---

### spaCy

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| Béjaïa → LOC ✅ | ALL dates ❌ | entreMme Warda HAMDI → PER ⚠️ (merged with "entreMme") |
| CPA → ORG ✅ | ALL CNI numbers ❌ | **Saida (standalone) → PER ❌** (should be LOC) |
| | 350 000 DA ❌ | DA → ORG ❌ (fragment of MONEY amount) |
| | | **Saida (CPA de) → ORG ❌** (should be LOC) |

**Speed:** 0.05s

---

### Flair

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| Warda HAMDI → PER ✅ | 27 Chaabane 1446 → full DATE ❌ | **Chaabane 1446 → MISC ⚠️** (partial, missing "27") |
| Nabil SAIDI → PER ✅ | 26/02/2025 → DATE ❌ | M → PER ⚠️ (fragment of "M.") |
| Béjaïa → LOC ✅ | 095384721 → CNI ❌ | CNI → ORG ⚠️ (label only) |
| Saida ×2 → LOC ✅ | 118273645 → CNI ❌ | |
| CPA → ORG ✅ | 350 000 DA → MONEY ❌ | |
| | 01/03/2025 → DATE ❌ | |

**Speed:** 0.55s

---

### GLiNER (threshold 0.3 / 0.5 / 0.7)

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| **27 Chaabane 1446 → date ✅** (0.72) — only model! | 350 000 DA → MONEY ❌ (no money label in GLiNER) | |
| **26/02/2025 → date ✅** (0.93) | | |
| **Warda HAMDI → person ✅** (0.86) | | |
| **CNI n° 095384721 → national id number ✅** (0.86) — correctly NOT date/phone | | |
| **M. Nabil SAIDI → person ✅** (0.99) | | |
| **CNI n° 118273645 → national id number ✅** (0.82) — correctly NOT date/phone | | |
| **Béjaïa → location ✅** (0.93) | | |
| **Saida → location ✅** (0.96) | | |
| **01/03/2025 → date ✅** (0.95) | | |
| agence CPA → organization (0.47, only at threshold 0.3) | | |
| **Saida → location ✅** (0.95) | | |

**Only model that handles ALL edge cases correctly** — Hijri date, Gregorian dates, CNI IDs as national_id_number (not date/phone), locations, people, and org.

**Speed:** 0.35–2.12s

---

### BERT-NER (dslim/bert-base-NER)

Heavy subword fragmentation. Not usable.

| Notable fragments |
|------------------|
| Ward → PER (partial), Nabil → PER (partial) |
| **SAID → ORG ❌** (should be PER — surname fragment) |
| Béjaïa → LOC ✅ (almost full) |
| Saida ×2 → LOC ✅ |
| CPA → ORG ✅ |

**Speed:** 1.77s

---

### CamemBERT

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| Warda HAMDI → PER ✅ | ALL dates ❌ | **Chaabane → MISC ⚠️** (partial — missing "27" and "1446") |
| Nabil SAIDI → PER ✅ | ALL CNI numbers ❌ | |
| Béjaïa → LOC ✅ | 350 000 DA → MONEY ❌ | |
| Saida ×2 → LOC ✅ | | |
| CPA → ORG ✅ | | |

**Speed:** 1.74s

---

### CAMeLBERT

Complete garbage on French text — 20 entities, mostly fragments. Not usable.

**Speed:** 0.57s

---

### GLiNER2 (fallback to GLiNER — model repo not found)

| Found ✅ | Missed ❌ |
|---------|----------|
| 26/02/2025 → date ✅ | **27 Chaabane 1446 → date ❌** (missed Hijri date that GLiNER @0.3 found) |
| Warda HAMDI → person ✅ | 350 000 DA → MONEY ❌ |
| CNI n° 095384721 → national id number ✅ | agence CPA ❌ |
| M. Nabil SAIDI → person ✅ | |
| CNI n° 118273645 → national id number ✅ | |
| Béjaïa → location ✅ | |
| Saida → location ✅ (standalone) | |
| 01/03/2025 → date ✅ | |
| Saida → location ✅ (CPA de Saida) | |

GLiNER2 miss **27 Chaabane 1446** — the Hijri date that GLiNER @0.3 found (score 0.72). Possibly due to slight difference in the fallback GLiNER version or aggregation strategy.

**Speed:** 1.87s

---

### Summary & Full Picture — Text 6

| Model | PERSON | LOCATION | ORG | DATE (Hijri) | DATE (Gregorian) | CNI/ID | MONEY | Arabic month handled? | Speed | Verdict |
|-------|---------|----------|-----|-------------|-------------------|--------|-------|---------------------|-------|---------|
| **Stanza** | ⚠️ Warda merged | ✅ | ✅ CPA | ❌ 27 Chaabane→LOC | ❌ | ❌ | ❌ | ❌ (LOC) | 0.53s | Weak on dates/IDs |
| **spaCy** | ⚠️ Warda merged | ⚠️ Saida→PER/ORG | ✅ CPA | ❌ | ❌ | ❌ | ❌ | N/A | **0.05s** | Fast but wrong types |
| **Flair** | ✅ | ✅ Saida×2 LOC | ✅ CPA | ⚠️ Chaabane→MISC partial | ❌ | ❌ | ❌ | ⚠️ partial | 0.55s | Decent but partial dates |
| **GLiNER** @0.3 | ✅ | ✅ | ⚠️ agence CPA (low conf) | **✅ 27 Chaabane 1446** | **✅ 26/02/2025** | **✅ both CNI** | ❌ | **✅** | 0.35-2.12s | **Best — only one with Hijri + Gregorian + CNI + both people** |
| **GLiNER2** | ✅ | ✅ | ❌ | ❌ missed | **✅** | **✅** | ❌ | ❌ missed | 1.87s | Good but missed Hijri date |
| **BERT-NER** | ⚠️ fragments | ✅ | ✅ CPA | ❌ | ❌ | ❌ | ❌ | ❌ | 1.77s | Fragments |
| **CamemBERT** | ✅ | ✅ Saida×2 LOC | ✅ CPA | ❌ Chaabane→MISC | ❌ | ❌ | ❌ | ❌ partial | 1.74s | Clean but no dates/IDs |
| **CAMeLBERT** | ❌ fragments | ❌ fragments | ❌ fragments | ❌ | ❌ | ❌ | ❌ | ❌ | 0.57s | Not usable |

**Key Takeaways for Text 6 (Mixed Calendar/IDs/Money):**
1. **GLiNER @0.3** is the clear winner — only model that detects **both Hijri and Gregorian dates**, both **CNI IDs** (correctly as national_id_number, not date/phone), both **people**, and both **Saida locations**
2. **No model** detects **"350 000 DA"** — money/currency is a blind spot for all tested models
3. **CNI numbers are safe from misclassification** — GLiNER tags them as `national id number`, and no other model falsely tags them as date/phone (they just miss them)
4. **"27 Chaabane 1446"** misclassified by all traditional models — Stanza says LOC, Flair says MISC (partial), others just ignore it
5. **GLiNER2 (fallback)** surprisingly missed the Hijri date that GLiNER @0.3 found — the fallback uses a slightly different underlying model

---

## TEXT 7 (Document 11 — Tribal/family names)

| Field | Value |
|-------|-------|
| **ID** | Text 7 |
| **Language** | French |
| **Topic** | Tribal/family names — Ouled Sidi Cheikh confederation |

**Edge cases:**
- **"Ouled Sidi Cheikh"** — tribal confederation name, could be MISC / ORG / PERSON depending on model
- **"Cheikh"** — appears both as religious title in "Cheikh BOUAMAMA" (part of person name) and in "Ouled Sidi Cheikh" (tribal name)
- **"Touati" (surname) vs "Touat" (place)** — same root, different entity types, adjacent in text
- **"Monsieur Cheikh BOUAMAMA"** — "Monsieur" is a title, should not be part of PER entity (or at least not required)

### Stanza

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| El Bayadh → LOC ✅ | **Ouled Sidi Cheikh → LOC ❌** (should be MISC — tribal confederation tagged as place) |
| Monsieur Cheikh BOUAMAMA → PER ✅ | |
| Aflou → LOC ✅ | |
| Belhadj TOUATI → PER ✅ | |
| Touat → LOC ✅ | |
| Gourara → LOC ✅ | |

**Speed:** 0.44s

---

### spaCy

Same as Stanza — Ouled Sidi Cheikh → LOC ❌, everything else correct.

**Speed:** 0.04s

---

### Flair

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| Bayadh → LOC ✅ (missing "El") | **Ouled Sidi Cheikh → PER ❌** (tribal confederation tagged as person) |
| Aflou → LOC ✅ | **Monsieur Cheikh → PER ⚠️** (partial — "BOUAMAMA" dropped!) |
| Belhadj TOUATI → PER ✅ | |
| Touat → LOC ✅ | |
| Gourara → LOC ✅ | |

**Speed:** 0.71s

---

### GLiNER (threshold 0.3 / 0.5 / 0.7)

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| **La famille Ouled Sidi Cheikh → organization ⚠️** (includes "La famille", but ORG is reasonable for a tribal confederation) | commerce → organization ❌ (false positive — common noun) |
| El Bayadh → location ✅ | |
| Monsieur Cheikh BOUAMAMA → person ✅ | |
| Aflou → location ✅ | |
| Belhadj TOUATI → person ✅ | |
| Touat → location ✅ | |
| Gourara → location ✅ (0.50 — only at 0.3 and 0.5, lost at 0.7) | |

GLiNER gives the most reasonable type for "Ouled Sidi Cheikh" (organization vs expected MISC). However, it includes "La famille" and has a false positive for "commerce".

**Speed:** 0.29–0.93s

---

### BERT-NER (dslim/bert-base-NER)

Heavy fragmentation. Not usable.

| Notable |
|---------|
| O → ORG (fragment), Sidi Cheikh → ORG (partial) |
| Chei → PER (fragment of Cheikh), ##OUAMAM → ORG (fragment of BOUAMAMA) |
| Belhad → PER (partial), To → PER (fragment of Touat) |

**Speed:** 1.24s

---

### CamemBERT

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| El Bayadh → LOC ✅ | **Ouled Sidi Cheikh → PER ❌** (tribal confederation as person) |
| **Cheikh BOUAMAMA → PER ✅** (clean — no "Monsieur" prefix! Best of all models) | |
| Aflou → LOC ✅ | |
| Belhadj TOUATI → PER ✅ | |
| Touat → LOC ✅ | |
| Gourara → LOC ✅ | |

**Best handling of "Cheikh BOUAMAMA"** — only model that correctly excludes "Monsieur" from the PER entity.

**Speed:** 1.09s

---

### CAMeLBERT

Complete garbage — 13 entities, mostly fragments. Not usable.

**Speed:** 0.33s

---

### GLiNER2 (fallback to GLiNER — model repo not found)

| Found ✅ | Missed ❌ |
|---------|----------|
| La famille Ouled Sidi Cheikh → organization ⚠️ | **Gourara → LOC ❌** (GLiNER @0.3 found it at 0.50) |
| El Bayadh → location ✅ | |
| Monsieur Cheikh BOUAMAMA → person ✅ | |
| Aflou → location ✅ | |
| Belhadj TOUATI → person ✅ | |
| Touat → location ✅ | |

**Speed:** 0.90s

---

### Summary & Full Picture — Text 7 (Tribal/family names)

| Model | Ouled Sidi Cheikh type | Cheikh BOUAMAMA | LOC (El Bayadh, Aflou, Touat, Gourara) | Touati/Touat distinction | Speed | Verdict |
|-------|------------------------|-----------------|----------------------------------------|--------------------------|-------|---------|
| **Stanza** | LOC ❌ | ✅ (with Monsieur) | All ✅ | ✅ | 0.44s | Good but wrong type on tribal name |
| **spaCy** | LOC ❌ | ✅ (with Monsieur) | All ✅ | ✅ | **0.04s** | Same as Stanza, faster |
| **Flair** | PER ❌ | ⚠️ dropped BOUAMAMA | ✅ (Gourara, Touat) | ✅ | 0.71s | Worst — lost the surname! |
| **GLiNER** @0.3/0.5 | **ORG ⚠️** (closest — reasonable for tribal confederation) | ✅ (with Monsieur) | ✅ (all 4) | ✅ | 0.29-0.93s | Most reasonable type for tribal name |
| **GLiNER2** | ORG ⚠️ | ✅ (with Monsieur) | ⚠️ missed Gourara | ✅ | 0.90s | Missed Gourara |
| **BERT-NER** | ⚠️ ORG fragments | ❌ fragments | ⚠️ partial | ❌ | 1.24s | Not usable |
| **CamemBERT** | PER ❌ | **✅ clean (no Monsieur)** | ✅ (all 4) | ✅ | 1.09s | **Best PER extraction — no "Monsieur" noise** |
| **CAMeLBERT** | ❌ fragments | ❌ fragments | ❌ fragments | ⚠️ Touat→PERS | 0.33s | Not usable |

**Key Takeaways for Text 7 (Tribal/family names):**
1. **No model** classifies "Ouled Sidi Cheikh" as MISC — closest is GLiNER with ORG (reasonable for a tribal confederation)
2. **CamemBERT** wins for clean PERSON extraction — only model that correctly excludes "Monsieur" from "Cheikh BOUAMAMA"
3. **Flair** is the worst — drops the surname "BOUAMAMA" entirely
4. **Touati/Touat distinction** handled correctly by all good models ✅
5. **No model has a MISC label** for this type of entity — tribal confederations fall between ORG and LOC

---

## TEXT 8 (Document 13 — Numbers/currency/IDs)

| Field | Value |
|-------|-------|
| **ID** | Text 8 |
| **Language** | French |
| **Topic** | Payment/vehicle/contact — money amounts, cheque, plate, phones, CNI, date |

**Edge cases:**
- **Algerian dinar written two ways** — "45 000 DA" vs "4 500 000 centimes" (same amount, different unit)
- **Cheque number "0023841"** — purely numeric, looks like an ID
- **"BEA"** — 3-letter bank acronym (Banque Extérieure d'Algérie)
- **License plate "30123-115-16"** — serial-daïra-wilaya format, "-16" = Skikda
- **Mobile vs landline** — "05 56 78 90 12" (mobile) vs "029 71 22 33" (landline)
- **CNI "200587412639"** — 12-digit number that a weak model could mistake for phone or date

### Stanza

| Found ✅ | Missed ❌ |
|---------|----------|
| Ouargla → LOC ✅ | 45 000 DA → MONEY ❌ |
| Tamanrasset → LOC ✅ | 4 500 000 centimes → MONEY ❌ |
| | 0023841 → cheque ❌ |
| | BEA → ORG ❌ |
| | 30123-115-16 → plate ❌ |
| | Skikda → LOC ❌ (merged as "Skikda.Contact") |
| | 05 56 78 90 12 → phone ❌ |
| | 029 71 22 33 → phone ❌ |
| | 200587412639 → CNI ❌ |
| | 14/06/2019 → DATE ❌ |

Only 2 LOC found out of 12 expected entities.

**Speed:** 0.20s

---

### spaCy

| Found ✅ | Wrong ⚠️ | Missed ❌ |
|---------|----------|---------|
| Ouargla → LOC ✅ | Montant → PER ❌ (field label) | 45 000 DA ❌ |
| **30123-115-16 → MISC ✅** (only model to find the plate!) | DA → ORG ❌ (MONEY fragment) | 4 500 000 centimes ❌ |
| wilaya de Skikda → LOC ✅ | Contact → LOC ❌ (field label) | 0023841 ❌ |
| Tamanrasset → LOC ✅ | CNI → ORG ⚠️ (label only) | BEA ❌ |
| | | 05 56 78 90 12 ❌ |
| | | 029 71 22 33 ❌ |
| | | 200587412639 ❌ |
| | | 14/06/2019 ❌ |

**Speed:** 0.04s

---

### Flair

| Found ✅ | Wrong ⚠️ | Missed ❌ |
|---------|----------|---------|
| Ouargla → LOC ✅ | DA → LOC ❌ (MONEY fragment) | Almost everything |
| Tamanrasset → LOC ✅ | wilaya de Skikda.Contact → LOC ❌ (merged) | |
| | CNI → ORG ⚠️ (label only) | |

Only 3 LOC-like entities found. Worst performer on this text.

**Speed:** 0.57s

---

### GLiNER (threshold 0.3 / 0.5 / 0.7)

| Found ✅ | Missed ❌ |
|---------|----------|
| **BEA agence de Ouargla → organization ✅** (0.84) | 45 000 DA → MONEY ❌ |
| **wilaya de Skikda → location ✅** (0.65) | 4 500 000 centimes → MONEY ❌ |
| **05 56 78 90 12 → phone number ✅** (0.99) | 0023841 → cheque ❌ |
| **029 71 22 33 → phone number ✅** (0.90) | 30123-115-16 → plate ❌ |
| **CNI n° 200587412639 → national id number ✅** (0.47 — only at 0.3) | |
| **14/06/2019 → date ✅** (0.99) | |
| **Tamanrasset → location ✅** (0.79) | |

Best performer with 7/12 entities. Still misses money amounts, cheque, and vehicle plate.

At threshold 0.5: loses CNI (0.47). At 0.7: also loses wilaya de Skikda (0.65).

**Speed:** 0.48–2.88s

---

### BERT-NER (dslim/bert-base-NER)

| Found ✅ | Fragments ⚠️ |
|---------|--------------|
| BEA → ORG ✅ (standalone! Only model to find BEA separately) | O → PER, ##ua → LOC (Ouargla fragments) |
| Tamanrasset → LOC ✅ | Ski → ORG, ##k → LOC, ##da → ORG (Skikda fragments) |
| CNI → ORG ⚠️ (label only) | V → ORG, w → PER (garbage) |

**Speed:** 1.83s

---

### CamemBERT

| Found ✅ | Missed ❌ |
|---------|----------|
| Ouargla → LOC ✅ | EVERYTHING else — no money, no phones, no IDs, no date, no org |
| **Skikda → LOC ✅** (clean — only model with clean "Skikda" without noise) | |
| Tamanrasset → LOC ✅ | |

Only 3 LOC entities found. Worst traditional model for this text type — zero non-LOC entities.

**Speed:** 1.03s

---

### CAMeLBERT

Complete garbage — 23 entities, mostly fragments. Not usable.

**Speed:** 0.41s

---

### GLiNER2 (fallback to GLiNER — model repo not found)

| Found ✅ | Missed ❌ |
|---------|----------|
| BEA agence de Ouargla → organization ✅ | wilaya de Skikda ❌ |
| 05 56 78 90 12 → phone number ✅ | CNI n° 200587412639 ❌ |
| 029 71 22 33 → phone number ✅ | 45 000 DA ❌ |
| 14/06/2019 → date ✅ | 4 500 000 centimes ❌ |
| Tamanrasset → location ✅ | 0023841 ❌ |
| | 30123-115-16 ❌ |

5/12 entities. Missed Skikda and CNI that GLiNER @0.3 found.

**Speed:** 2.77s

---

### Summary & Full Picture — Text 8 (Numbers/currency/IDs)

| Model | MONEY | CHEQUE | ORG (BEA) | LOC | PLATE | PHONE (mobile) | PHONE (landline) | CNI | DATE | Entities found | Speed | Verdict |
|-------|-------|--------|-----------|-----|-------|----------------|------------------|-----|------|---------------|-------|---------|
| **Stanza** | ❌ | ❌ | ❌ | ✅ Ouargla, Tamanrasset (2/4) | ❌ | ❌ | ❌ | ❌ | ❌ | 2/12 | 0.20s | Missed everything numeric |
| **spaCy** | ❌ | ❌ | ❌ | ✅ Ouargla, Skikda, Tamanrasset (3/4) | **✅** (merged) | ❌ | ❌ | ❌ | ❌ | 4/12 | **0.04s** | **Only model with plate** |
| **Flair** | ❌ | ❌ | ❌ | ⚠️ merged Skikda (2/4) | ❌ | ❌ | ❌ | ❌ | ❌ | 2/12 | 0.57s | Very poor |
| **GLiNER** @0.3 | ❌ | ❌ | ✅ BEA agence | ✅ Skikda, Tamanrasset (2/4) | ❌ | **✅** | **✅** | **✅** (0.47) | **✅** | **7/12** | 0.48-2.88s | **Best — phones + CNI + date + ORG** |
| **GLiNER2** | ❌ | ❌ | ✅ BEA agence | ⚠️ only Tamanrasset (1/4) | ❌ | **✅** | **✅** | ❌ | **✅** | 5/12 | 2.77s | Good but missed CNI + Skikda |
| **BERT-NER** | ❌ | ❌ | **✅ BEA standalone** | ⚠️ fragments (1/4) | ❌ | ❌ | ❌ | ❌ | ❌ | 3/12 | 1.83s | BEA standalone only win |
| **CamemBERT** | ❌ | ❌ | ❌ | ✅ 3/4 clean | ❌ | ❌ | ❌ | ❌ | ❌ | 3/12 | 1.03s | LOC only — worst on non-LOC |
| **CAMeLBERT** | ❌ | ❌ | ❌ | ❌ fragments | ❌ | ❌ | ❌ | ❌ | ❌ | 0/12 | 0.41s | Not usable |

**Key Takeaways for Text 8 (Numbers/currency/IDs):**
1. **GLiNER @0.3** wins but still only finds 7/12 — phones, date, CNI, ORG, and some LOC
2. **No model** detects **money amounts** ("45 000 DA", "4 500 000 centimes") — money remains a complete blind spot across all models
3. **No model** detects **cheque number** "0023841"
4. **Vehicle plate** "30123-115-16" — only **spaCy** finds it (merged with extra text)
5. **BEA** — only **BERT-NER** finds it standalone; GLiNER gets it as "BEA agence de Ouargla"
6. **CamemBERT** only finds LOC — doesn't detect phones, dates, IDs, or orgs at all on this text
7. **Traditional NER models** (Stanza, spaCy, Flair, CamemBERT) are near-useless on numeric-heavy documents — they only catch location names

---

## TEXT 9 (Document 16 — OCR noisy scanned doc)

| Field | Value |
|-------|-------|
| **ID** | Text 9 |
| **Language** | French |
| **Topic** | OCR-scanned residence certificate — ALL-CAPS, no spaces between entities |

**Edge cases:**
- **ALL-CAPS text** — removes the capitalization cue most NER models rely on
- **No spaces between entities** — "POPULAIREWILAYA", "OULMENECOMMUNE", "BIR HADDADACERTIFICAT", "2024/0417NOM", "ABDELKRIMNE(E)", "SETIFDEMEURANT" — OCR merged everything
- **Extra OCR spacing** — "DE  BIR  HADDADA" (double spaces), "HAMMAM  SOKHNA", "DAIRA  DE  AIN  OULMENE"
- **Multi-level admin hierarchy** — Wilaya → Daira → Commune all place-like words
- **Labels with colons** — "NOM:", "PRENOM(S):", "NE(E) LE:", "A:"

### Stanza

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| HAMMAM  SOKHNA → LOC ✅ | REPUBLIQUE ALGERIENNE → ORG ❌ (country as org), DEMOCRATIQUE → ORG (fragment) |
| DAIRA  DE  AIN  OULMENE → LOC ✅ | POPULAIREWILAYA DE SETIF → ORG ❌ (merged, wrong type) |
| | KADDOUR → ORG ❌ (surname as org!) |
| | Most entities merged or fragmented |

**Speed:** 0.78s

---

### spaCy

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| HAMMAM  SOKHNA → LOC ✅ | Almost everything merged into giant MISC spans |
| OULMENE → LOC ✅ (partial) | POPULAIREWILAYA DE SETIF → MISC (merged) |
| | KADDOUR → LOC ❌ (surname as location!) |
| | ABDELKRIMNE(E → LOC ❌ (merged with label) |

**Speed:** 0.05s

---

### Flair

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| REPUBLIQUE ALGERIENNE DEMOCRATIQUE → ORG ⚠️ (country as org) | Most entities merged into neighbour text due to missing spaces |
| SETIF → LOC ✅ (clean!) | POPULAIREWILAYA → MISC (merged), DAIRA DE AIN OULMENECOMMUNE → LOC (merged) |
| HAMMAM  SOKHNA → LOC ✅ | 2024/0417NOM: KADDOUR → merged mess |
| DAIRA  DE  AIN  OULMENE → LOC ✅ | ABDELKRIMNE merged with "NE(E) LE:" |

**Speed:** 0.55s

---

### GLiNER (threshold 0.3 / 0.5 / 0.7)

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| **KADDOUR → person ✅** (0.57) — only model to find surname correctly! | REPUBLIQUE...POPULAIREWILAYA DE SETIF → organization ❌ (merged 2 entities) |
| **03 01 1980 → date ✅** (0.94) — only model to find date with spaces! | HAMMAM  SOKHNA → person ❌ (should be LOC) |
| | SETIFDEMEURANT → location ❌ (merged with label) |
| | DAIRA  DE  AIN  OULMENE → person ❌ (should be LOC) |

At 0.5: loses KADDOUR (0.57), SETIFDEMEURANT (0.41), DAIRA (0.41).
At 0.7: only date + HAMMAM remain.

**Speed:** 0.34–0.81s

---

### BERT-NER (dslim/bert-base-NER)

Heavy fragmentation. Not usable.

**Speed:** 1.78s

---

### CamemBERT

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| **REPUBLIQUE ALGERIENNE DEMOCRATIQUE ET POPULAIRE → LOC ✅** (country correct despite ALL-CAPS! Only model) | WILAYA DE SETIF → PER ❌ (admin unit as person) |
| DAIRA DE AIN OULMENECOMMUNE DE BIR HADD → LOC ⚠️ (merged, no space after OULMENE) | KADDOUR → PER ✅ (but merged span boundaries) |
| AIN OULMENE → LOC ✅ (clean at end) | ABDELKRIMNE → PER ⚠️ (merged with "NE(E)") |
| | HAMMAM SOKHNA → PER ❌ (should be LOC) |
| | DAIRA DE → PER ❌ (fragment) |

**Best model for this text** — only one to correctly identify the country name despite ALL-CAPS and no spaces.

**Speed:** 1.71s

---

### CAMeLBERT

Complete garbage — fragments only. Not usable.

**Speed:** 0.42s

---

### GLiNER2 (fallback to GLiNER — model repo not found)

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| 03 01 1980 → date ✅ | REPUBLIQUE...POPULAIREWILAYA DE SETIF → organization ❌ (merged) |
| | HAMMAM  SOKHNA → person ❌ (should be LOC) |

Only 3 entities found. Worst coverage on this text.

**Speed:** 0.70s

---

### Summary & Full Picture — Text 9 (OCR noisy / ALL-CAPS)

| Model | Country (RADP) | Wilaya / Daira / Commune | Certificate N° | PERSON (Kaddour, Abdelkrim) | Date (03 01 1980) | LOC (Sétif, Hammam Sokhna) | Handles ALL-CAPS? | Handles no-spaces OCR? | Speed | Verdict |
|-------|---------------|--------------------------|----------------|----------------------------|-------------------|---------------------------|-------------------|----------------------|-------|---------|
| **Stanza** | ❌ ORG | ❌ merged | ❌ | ❌ KADDOUR→ORG | ❌ | ✅ Hammam, Daira | ❌ | ❌ | 0.78s | OCR breaks it |
| **spaCy** | ❌ | ❌ merged | ❌ | ❌ merged | ❌ | ✅ Hammam, partial Oulmene | ❌ | ❌ | **0.05s** | All merged into MISC |
| **Flair** | ⚠️ ORG | ❌ merged | ❌ | ❌ merged | ❌ | ✅ SETIF, Hammam, Daira | ❌ | ❌ | 0.55s | Partial LOC OK |
| **GLiNER** @0.3 | ❌ merged | ❌ merged | ❌ | **✅ KADDOUR** | **✅ 03 01 1980** | ❌ wrong types (person) | ⚠️ finds some | ❌ | 0.34-0.81s | **Only model with date + surname** |
| **GLiNER2** | ❌ merged | ❌ | ❌ | ❌ | **✅** | ❌ wrong types | ❌ | ❌ | 0.70s | Worst — only 3 entities |
| **BERT-NER** | ❌ | ❌ fragments | ❌ | ❌ | ❌ | ❌ fragments | ❌ | ❌ | 1.78s | Not usable |
| **CamemBERT** | **✅ LOC** (only model!) | ⚠️ merged but partially found | ❌ | ⚠️ merged with labels | ❌ | ⚠️ wrong types (PER) | **✅ best** | ❌ but best effort | 1.71s | **Best — only model to identify country correctly** |
| **CAMeLBERT** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | 0.42s | Not usable |

**Key Takeaways for Text 9 (OCR noisy / ALL-CAPS):**
1. **CamemBERT** is the best — only model to correctly identify **"REPUBLIQUE ALGERIENNE DEMOCRATIQUE ET POPULAIRE" as LOC** despite ALL-CAPS and no spaces
2. **GLiNER @0.3** is the only model with **date** ("03 01 1980") and **surname** ("KADDOUR")
3. **Missing spaces between entities** is catastrophic — every model merges "POPULAIREWILAYA", "OULMENECOMMUNE", "SETIFDEMEURANT"
4. **ALL-CAPS alone** is manageable (CamemBERT handles it), but **no spaces + ALL-CAPS** together destroys all models
5. **Pre-processing needed** — splitting on uppercase boundaries and adding spaces before NER would fix most issues
6. **"2024/0417" (certificate)** — zero models find it
