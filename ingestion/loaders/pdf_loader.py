"""
pdf_loader.py — PDF loader via PyMuPDF
"""

from pathlib import Path

from ingestion.base import AbstractDocumentLoader
from ingestion.exceptions import IngestionError


class PdfLoader(AbstractDocumentLoader):
    """Extract text from every page of a PDF."""

    def load(self, path: Path) -> str:
        try:
            import fitz
        except ImportError:
            raise IngestionError("PyMuPDF (fitz) is required to read PDFs.")

        try:
            doc = fitz.open(path)
        except Exception as exc:
            raise IngestionError(f"Failed to open PDF {path}: {exc}")

        pages = []
        for page in doc:
            pages.append(page.get_text())
        doc.close()

        return "\f".join(pages)
