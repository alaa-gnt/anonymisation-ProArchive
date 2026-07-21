from src.pipeline import anonymize_file

SEP = "=" * 70

print(SEP)
print("  STEP 1 — OCR + Anonymize sample_1.png")
print(SEP)

result, meta = anonymize_file("samples/sample_1.png")

print(f"\n  Source : {meta['filename']}")
print(f"  Type   : {meta['extension']}")
print(f"  Chars  : {meta['char_count']}")
if 'lines' in meta:
    print(f"  Lines  : {meta['lines']}")

print(f"\n{SEP}")
print("  STEP 2 — Anonymized Output")
print(SEP)

print(f"\n{result.text}")

print(f"{SEP}")
print(f"  Original chars : {meta['char_count']}")
print(f"  Output  chars  : {len(result.text)}")
print(f"{SEP}")
