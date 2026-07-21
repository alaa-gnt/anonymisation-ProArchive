from ingestion import read_file

FILES = [
    "samples/sample.txt",
    "samples/sample.pdf",
    "samples/sample_1.png",
]

SEPARATOR = "=" * 60

for path in FILES:
    try:
        text, meta = read_file(path)

        print(SEPARATOR)
        print(f"  FILE   : {meta['filename']}")
        print(f"  TYPE   : {meta['extension']}")
        print(f"  SOURCE : {meta['source']}")
        print(f"  CHARS  : {meta['char_count']}")

        extra_keys = [k for k in meta if k not in ("source", "extension", "filename", "char_count")]
        for k in extra_keys:
            print(f"  {k.upper():6s}: {meta[k]}")

        print()
        print(f"  ── BLOCKS ({len(text.splitlines())} lines) ──")
        print(text.rstrip())

    except Exception as e:
        print(SEPARATOR)
        print(f"  FILE   : {path}")
        print(f"  ERROR  : {e}")

    print()
