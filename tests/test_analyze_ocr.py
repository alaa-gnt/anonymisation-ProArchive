from src.analyzer import get_analyzer, run_analyzer
from ingestion import read_file

text, meta = read_file("samples/sample_1.png")

analyzer = get_analyzer()
results = run_analyzer(analyzer, text, language="fr")

print(f"Source : {meta['filename']}")
print(f"Chars  : {meta['char_count']}")
print()

for r in sorted(results, key=lambda x: x.start):
    print(f"  {r.entity_type:20s}  [{r.start:3d}:{r.end:3d}]  {text[r.start:r.end]:45s}  score={r.score}")
