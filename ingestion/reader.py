"""
reader.py — Document Ingestion Facade
======================================

Detects file type by extension and dispatches to the correct loader.

Usage:
    from ingestion.reader import read_file

    text, meta = read_file("contract.pdf")
    print(meta["source"], meta["extension"])
"""

from pathlib import Path

from ingestion.exceptions import UnsupportedFormatError
from ingestion.loaders import LOADERS


def read_file(path):
    """
    Detect file type and extract text.

    Parameters
    ----------
    path : str or Path
        Path to the document.

    Returns
    -------
    (text, metadata)
        text : str — full extracted text.
        metadata : dict — source path, extension, filename, char_count.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    UnsupportedFormatError
        If the extension is not registered.
    """
    path = Path(path)
    ext = path.suffix.lower()

    loader = LOADERS.get(ext)
    if loader is None:
        raise UnsupportedFormatError(
            f"Unsupported file extension '{ext}'. "
            f"Supported: {', '.join(sorted(LOADERS.keys()))}"
        )

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    text = loader.load(path)

    metadata = {
        "source": str(path.resolve()),
        "extension": ext,
        "filename": path.name,
        "char_count": len(text),
    }

    return text, metadata
