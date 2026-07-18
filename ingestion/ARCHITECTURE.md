# Ingestion Layer — Architecture

```
                        ┌──────────────────────────┐
                        │       read_file(path)      │
                        │       (entry point)        │
                        └────────────┬─────────────┘
                                     │
                                     ▼
                        ┌──────────────────────────┐
                        │    1. Validate path       │
                        │       exists?             │
                        └────────────┬─────────────┘
                                     │
                                     ▼
                        ┌──────────────────────────┐
                        │    2. Detect extension    │
                        │       .pdf ?  .docx ?     │
                        └────────────┬─────────────┘
                                     │
                   ┌─────────────────┼─────────────────┐
                   ▼                 ▼                  ▼
        ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
        │  PDF Loader      │ │  DOCX Loader │ │  TXT Loader      │
        │  (PyMuPDF)       │ │ (python-docx)│ │  (built-in open) │
        │                  │ │              │ │                  │
        │  pages_text = [] │ │  paragraphs  │ │  try utf-8       │
        │  for page in doc │ │  = [p.text   │ │  fallback latin-1│
        │    pages_text    │ │    for p in  │ │  fallback cp1256  │
        │    .append(      │ │    doc.para- │ │                  │
        │    page.get_text │ │    graphs]   │ │  return text      │
        │    ())           │ │              │ │                  │
        │  return text     │ │  return text │ │                  │
        └────────┬─────────┘ └──────┬───────┘ └────────┬─────────┘
                 │                  │                   │
                 └──────────────────┼───────────────────┘
                                    │
                                    ▼
                        ┌──────────────────────────┐
                        │    3. Assemble metadata   │
                        │       source, extension,  │
                        │       char_count, pages   │
                        └────────────┬─────────────┘
                                     │
                                     ▼
                        ┌──────────────────────────┐
                        │  return (text, metadata)  │
                        └──────────────────────────┘
```

---

## Module Structure

```
ingestion/
│
├── __init__.py          # exports read_file() + UnsupportedFormatError
│
├── reader.py            # Facade — validates path, detects extension,
│                        # dispatches to the right loader
│
├── ARCHITECTURE.md      # This file
│
├── exceptions.py        # UnsupportedFormatError, IngestionError
│
├── base.py              # AbstractDocumentLoader (ABC)
│
└── loaders/
    ├── __init__.py       # loader registry dict
    ├── txt_loader.py     # .txt .md .csv .json .xml .html
    ├── pdf_loader.py     # .pdf
    ├── docx_loader.py    # .docx
    └── image_loader.py   # .png .jpg .jpeg .tiff
```

---

## Adding a New Format

```
1. Create  ingestion/loaders/foo_loader.py
2. Implement  class FooLoader(AbstractDocumentLoader)
3. Register   LOADERS[".foo"] = FooLoader()
```

No other file needs to change. That is the whole point of this architecture.
