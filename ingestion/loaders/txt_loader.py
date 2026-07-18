"""
txt_loader.py — Plain-text loader (.txt, .md, .csv, .json, .xml, .html)
"""

from pathlib import Path

from ingestion.base import AbstractDocumentLoader
from ingestion.exceptions import IngestionError


class TxtLoader(AbstractDocumentLoader):
    """Read text files with automatic encoding detection."""

    ENCODINGS = ["utf-8", "latin-1", "windows-1256"]

    def load(self, path: Path) -> str:
        for enc in self.ENCODINGS:
            try:
                with open(path, "r", encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise IngestionError(f"Could not decode {path} with any known encoding.")
