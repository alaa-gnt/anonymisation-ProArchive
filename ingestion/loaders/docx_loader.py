"""
docx_loader.py — Word document loader via python-docx
"""

from pathlib import Path

from ingestion.base import AbstractDocumentLoader
from ingestion.exceptions import IngestionError


class DocxLoader(AbstractDocumentLoader):
    """Extract text from a .docx file."""

    def load(self, path: Path) -> str:
        try:
            from docx import Document
        except ImportError:
            raise IngestionError("python-docx is required to read .docx files.")

        try:
            doc = Document(str(path))
        except Exception as exc:
            raise IngestionError(f"Failed to open docx {path}: {exc}")

        paragraphs = [p.text for p in doc.paragraphs]
        return "\n".join(paragraphs)
