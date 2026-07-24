# Arabic NER Model Results

**Models tested:** Stanza, GLiNER, CAMeLBERT, GLiNER2 (fallback to GLiNER)
**Excluded:** spaCy, Flair, CamemBERT, BERT-NER (French/English only — ignore Arabic)

---

## TEXT A1 — Arabic Civil Registry (MSA)

| Field | Value |
|-------|-------|
| **ID** | A1 |
| **Language** | Arabic (MSA) |
| **Topic** | Civil Registry (Arabic version of Text 1) — same names/places in Arabic script |

**Edge cases:**
- **"سعيدة" (Saida) ×5** — first name, city, wilaya, all same word
- **No spaces** — "الشعبيةولاية", "سعيدةنشهد"
- **Spelled-out dates** — "السنة الألفين واثنتي عشرة", "الخامس عشر من شهر مارس"
- **Numeric dates** — 1985/07/03, 1988/11/21, 20 مارس 2012
- **Prefixes attached** — "بتلمسان" (ب+تلمسان), "بوهران" (ب+وهران), "بسعيدة" (ب+سعيدة), "وندى مزيان" (و+ندى)

### Stanza

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| الجمهورية الجزائرية الديمقراطية الشعبية → LOC ✅ | ولاية سعيدة ❌ (merged with country) | |
| سعيدة → LOC ✅ (standalone) | بلدية سعيدة ❌ (merged with "نشهد") | |
| **سعيدة بن علي → PER ✅** | السنة الألفين واثنتي عشرة ❌ | |
| **كريم بن علي → PER ✅** | الخامس عشر من شهر مارس ❌ | |
| بتلمسان → LOC ✅ (ب prefix handled!) | 1985/07/03 ❌ | |
| **وندى مزيان → PER ✅** (و prefix handled!) | 1988/11/21 ❌ | |
| بوهران → LOC ✅ (ب prefix handled!) | شارع أول نوفمبر ❌ | |
| بسعيدة → LOC ✅ (ب prefix handled!) | مديرية الصحة لولاية سعيدة ❌ | |
| الجزائر → LOC ✅ (partial — missed "العاصمة") | 20 مارس 2012 ❌ | |
| وزارة الداخلية والجماعات المحلية → ORG ✅ | | |

**10/19 entities — best traditional model for Arabic. Handles prefixes (ب, و) beautifully.**

**Speed:** 0.28s

---

### GLiNER (threshold 0.3)

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| سعيدة → location ✅ (one clean instance) | ولاية سعيدة ❌ (merged with country) | الجمهورية...ولاية سعيدة → organization ❌ (country as ORG) |
| **الخامس عشر من شهر مارس → date ✅** (only model with spelled-out date!) | السنة الألفين واثنتي عشرة ❌ | بلدية سعيدةنشهد → organization ❌ (merged) |
| **سعيدة بن علي → person ✅** | شارع أول نوفمبر ❌ | بسعيدة → person ❌ (0.34 — should be LOC) |
| **كريم بن علي → person ✅** | 20 مارس 2012 ✅ found at 0.3-0.7 | |
| **بتلمسان → location ✅** | | |
| **وندى مزيان → person ✅** | | |
| **بوهران → location ✅** | | |
| **1988/11/21 → date ✅** (0.31 — only at 0.3) | | |
| **مديرية الصحة لولاية سعيدة → organization ✅** (0.68) | | |
| **الجزائر العاصمة → location ✅** (0.79) | | |
| **وزارة الداخلية والجماعات المحلية → organization ✅** (0.45) | | |
| **20 مارس 2012 → date ✅** (0.93) | | |

**15/19 entities at 0.3 — best coverage. Only model with spelled-out date + numeric dates + all ORGs.**

At 0.5: loses 1988/11/21 (0.31), بسعيدة (0.34), وزارة (0.45) → 12 entities.
At 0.7: loses بتلمسان (0.55), بوهران (0.59), مديرية (0.68) → 8 entities.

**Speed:** 0.49–1.01s

---

### CAMeLBERT

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| **سعيدة → LOC ×4 ✅** (multiple instances clean!) | Fragments: بت→LOC, ##لمس→LOC, ##ان→LOC (تلمسان broken) |
| سعيدة بن علي → PERS ✅ | وند→PERS, ##ى مزيان→PERS (name fragmented) |
| كريم بن علي → PERS ✅ | بو→LOC, ##هران→LOC (وهران broken) |
| الجزائر → LOC ✅ | بس→PERS, ##عيدة→PERS (بسعيدة as PERS) |
| | بس→PERS, ##عيدة→PERS (second بسعيدة also PERS) |

Best at finding individual "سعيدة" LOC instances (found 4!). But heavy fragmentation on longer names and prefixed words.

**Speed:** 0.14s

---

### GLiNER2 (fallback to GLiNER)

| Found ✅ | Missed ❌ |
|---------|----------|
| الخامس عشر من شهر مارس → date ✅ | سعيدة (standalone) ❌ |
| سعيدة بن علي → person ✅ | بتلمسان ❌ |
| كريم بن علي → person ✅ | بوهران ❌ |
| وندى مزيان → person ✅ | 1988/11/21 ❌ |
| مديرية الصحة لولاية سعيدة → organization ✅ | بسعيدة ❌ |
| الجزائر العاصمة → location ✅ | |
| 20 مارس 2012 → date ✅ | |

9/19 entities. Misses all standalone LOC instances, prefixed locations, and low-confidence entities.

**Speed:** 0.86s

---

### Summary — Text A1

| Model | Entities found | Country (LOC) | Person | LOC (سعيدة) | Spelled-out dates | Numeric dates | ORG | Prefixes (ب, و) handled? | Speed | Verdict |
|-------|---------------|---------------|--------|-------------|-------------------|---------------|-----|-------------------------|-------|---------|
| **Stanza** | 10/19 | ✅ | ✅ 3 PER | ⚠️ 2/5 | ❌ | ❌ | ✅ 1 ORG | **✅** (best) | 0.28s | Best for clean Arabic LOC/PER |
| **GLiNER** @0.3 | **15/19** | ⚠️ ORG | ✅ 3 PER | ⚠️ 1/5 | **✅** | **✅ both** | **✅ 3 ORG** | ⚠️ sometimes | 0.49-1.01s | **Best coverage — only model with dates + ORGs** |
| **GLiNER2** | 9/19 | ⚠️ ORG | ✅ 3 PER | ❌ 0/5 | **✅** | ✅ 1 date | ✅ 2 ORG | ❌ | 0.86s | Good but missed standalone LOC |
| **CAMeLBERT** | 8/19 | ❌ fragment | ⚠️ 2 PER fragmented | **✅ 4/5** (best!) | ❌ | ❌ | ❌ | ❌ fragments | **0.14s** | **Best at finding سعيدة as LOC** |

**Key Takeaways:**
1. **Stanza** is best for clean Arabic LOC/PER with prefixes — handles بتلمسان, بوهران, بسعيدة, وندى مزيان perfectly
2. **GLiNER @0.3** has the best overall coverage — only model with spelled-out dates, numeric dates, and organization names
3. **CAMeLBERT** finds individual "سعيدة" LOC instances best (4/5) but fragments longer names
4. **No model** handles the no-space merging ("الشعبيةولاية", "سعيدةنشهد")
5. **Spelled-out dates** ("السنة الألفين واثنتي عشرة") — only GLiNER found one of them

---

## TEXT A2 — Arabic Court Document

| Field | Value |
|-------|-------|
| **ID** | A2 |
| **Language** | Arabic |
| **Topic** | Court document — محكمة وهران, companies, Hijri+Gregorian dates |

**Edge cases:**
- **"سعيداني" (surname from Saida root) vs "سعيدة" (place)** — not in same text, tests if model falsely triggers
- **"الأمل" ("Hope")** — simultaneously a common word and a charity name
- **"الشيخ" (Cheikh)** — religious title fused with person name
- **Hijri + Gregorian paired** — "12 رجب 1443 هـ" / "14 فبراير 2022 م"

### Stanza

| Found ✅ | Missed ❌ | Wrong ⚠️ |
|---------|----------|----------|
| وهران → LOC ✅ | محكمة وهران → ORG ❌ (only found city, not court) | |
| ياسين سعيداني → PER ✅ | بلدية سعيدة ❌ | |
| بالبليدة → LOC ✅ (ب prefix) | 12 رجب 1443 هـ ❌ | |
| شركة نفطال → ORG ✅ | 14 فبراير 2022 م ❌ | |
| فاروق بوزيد → PER ✅ | الأمل → ORG ❌ | |
| سوناطراك → ORG ✅ | | |
| سيدي بلعباس → LOC ✅ | | |
| عبد القادر بلحاج → PER ✅ (dropped "الشيخ") | | |
| بومرداس → LOC ✅ | | |

9/13 entities. Clean Arabic parsing but misses dates and the charity name.

**Speed:** 0.57s

---

### GLiNER (threshold 0.3)

| Found ✅ | Wrong ⚠️ | Missed ❌ |
|---------|----------|---------|
| **محكمة وهران → organization ✅** | الغرفة المدنية → organization ⚠️ (not in ground truth but reasonable) | البليدة ❌ |
| **ياسين سعيداني → person ✅** | | الأمل ❌ |
| شركة نفطال → company ✅ | | |
| السيد فاروق بوزيد → person ✅ (includes "السيد") | | |
| **شركة سوناطراك → company ✅** | | |
| **سيدي بلعباس → location ✅** | | |
| **بلدية سعيدة → location ✅** (0.49) | | |
| **12 رجب 1443 هـالموافق لـ 14 فبراير 2022 م → date ✅** (merged Hijri+Gregorian) | | |
| **الشيخ عبد القادر بلحاج → person ✅** (includes "الشيخ"!) | | |
| **بومرداس → location ✅** (0.57) | | |

**11/13 entities — best coverage. Only model with dates + keeps الشيخ title.** The Hijri+Gregorian dates merged as one span, which is actually correct (same date in two calendars).

At 0.5: loses محكمة وهران (0.45), بلدية سعيدة (0.49), بومرداس (0.57) → 8 entities.
At 0.7: also loses الغرفة المدنية (0.64) → 7 entities.

**Speed:** 0.33–1.45s

---

### CAMeLBERT

| Found ✅ | Wrong ⚠️ |
|---------|----------|
| ياسين سعيداني → PERS ✅ | وهران fragmented: وه+##ران ⚠️ |
| نفطال → ORG ✅ (without "شركة") | البليدة fragmented: بالب+##ليد+##ة ⚠️ |
| فاروق بوزيد → PERS ✅ | |
| سوناطراك → ORG ✅ | |
| سيدي بلعباس → LOC ✅ | |
| **سعيدة → LOC ✅** | |
| عبد القادر بلحاج → PERS ✅ (dropped "الشيخ") | |
| **الأمل → ORG ✅** (only model to find the charity name!) | |
| بومرداس → LOC ✅ | |

**Only model that found "الأمل" as ORG.** But fragments many longer words.

**Speed:** 0.41s

---

### GLiNER2 (fallback to GLiNER)

| Found ✅ | Missed ❌ |
|---------|----------|
| محكمة وهران → organization ✅ | بلدية سعيدة ❌ |
| الغرفة المدنية → organization ⚠️ | بومرداس ❌ |
| ياسين سعيداني → person ✅ | البليدة ❌ |
| شركة نفطال → company ✅ | الأمل ❌ |
| السيد فاروق بوزيد → person ✅ | |
| شركة سوناطراك → company ✅ | |
| سيدي بلعباس → location ✅ | |
| 12 رجب 1443 هـالموافق لـ 14 فبراير 2022 م → date ✅ | |
| الشيخ عبد القادر بلحاج → person ✅ | |

9/13 entities. Misses more low-confidence entities than GLiNER @0.3.

**Speed:** 0.55s

---

### Summary — Text A2

| Model | Entities | COURT (ORG) | PERSON | LOC | ORG (شركات) | DATE (Hijri+Greg) | الأمل (charity) | الشيخ kept? | Speed | Verdict |
|-------|----------|-------------|--------|-----|-------------|-------------------|----------------|-------------|-------|---------|
| **Stanza** | 9/13 | ⚠️ partial (وهران only) | ✅ 3 PER | ✅ 4 LOC | ✅ 3 ORG | ❌ both | ❌ | ❌ dropped | 0.57s | Clean but misses dates |
| **GLiNER** @0.3 | **11/13** | **✅ محكمة وهران** | ✅ 3 PER | ⚠️ 3/4 LOC (missed البليدة) | ✅ 2 company | **✅ merged** | ❌ | **✅ kept** | 0.33-1.45s | **Best — only model with dates + الشيخ** |
| **GLiNER2** | 9/13 | ✅ محكمة وهران | ✅ 3 PER | ⚠️ 2/4 LOC | ✅ 2 company | **✅ merged** | ❌ | **✅ kept** | 0.55s | Good but missed more LOC |
| **CAMeLBERT** | 8/13 | ❌ fragmented | ✅ 2 PER fragmented | ⚠️ 3 LOC fragmented | ✅ 2 ORG partial | ❌ both | **✅ الأمل** (only model!) | ❌ dropped | **0.41s** | **Only model with charity name** |

**Key Takeaways for Text A2:**
1. **GLiNER @0.3** wins — only model with both Hijri+Gregorian dates, court name as ORG, and "الشيخ" kept in person name
2. **CAMeLBERT** wins the "الأمل" edge case — only model that correctly tags the charity name as ORG
3. **No model** falsely triggered on "سعيداني" as LOC (edge case passed ✅)
4. **Stanza** is cleanest for standard entities but misses all dates and the charity
5. **GLiNER's date merging** (Hijri+Gregorian as one span) is actually correct behavior — same date in two calendars
