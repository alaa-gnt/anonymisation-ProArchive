from src.analyzer import get_analyzer, run_analyzer

analyzer = get_analyzer()

# Mixed Arabic/French realistic texts
texts = [
    # Carte d'identité nationale
    """REPUBLIQUE ALGERIENNE DEMOCRATIQUE ET POPULAIRE
CARTE D'IDENTITE NATIONALE
NIN: 104332181960013388
Nom: SLIMANI
Prénom: Abdellah
alaa
Né le: 15/03/1990 à Alger
Tél: 0551234567
Email: abdellah.slimani@example.com""",

    # Passeport algérien
    """الجمهورية الجزائرية الديمقراطية الشعبية
جواز سفر
رقم الجواز: 646253010
الاسم: عبد الله سليماني
تاريخ الميلاد: 15/03/1990
رقم التعريف الوطني: 104332181960013388
الهاتف: 0551234567""",

    # Document fiscal d'entreprise
    """Entreprise: SARL EL BARAKA
NIF: 499390892613715
NIS: 041659152017774
RC: 20/01-886365
RIB: 94856257287032032074
IBAN: DZ6227617075877712151342
Tél: 023456789
Adresse: 5 Rue Didouche Mourad, 16000 Alger""",
]

for i, text in enumerate(texts):
    print("=" * 60)
    print(f"  Document {i+1}")
    print("=" * 60)
    print(text)
    print()

    results = run_analyzer(analyzer, text, language="fr")
    if not results:
        results = run_analyzer(analyzer, text, language="ar")
    if not results:
        results = run_analyzer(analyzer, text, language="en")

    for r in sorted(results, key=lambda x: x.start):
        snippet = text[r.start:r.end]
        print(f"  {r.entity_type:20s}  {snippet:40s}  score={r.score:.2f}")
    print()
