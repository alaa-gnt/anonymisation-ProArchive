from src.pipeline import anonymize

texts = [
    """REPUBLIQUE ALGERIENNE DEMOCRATIQUE ET POPULAIRE
CARTE D'IDENTITE NATIONALE
NIN: 104332181960013388
Nom: SLIMANI
Prénom: Abdellah
Né le: 15/03/1990 à Alger
Tél: 0551234567
Email: abdellah.slimani@example.com""",

    """الجمهورية الجزائرية الديمقراطية الشعبية
جواز سفر
رقم الجواز: 646253010
الاسم: عبد الله سليماني
تاريخ الميلاد: 15/03/1990
رقم التعريف الوطني: 104332181960013388
الهاتف: 0551234567""",

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
    result = anonymize(text)
    print(result.text)
    print()
