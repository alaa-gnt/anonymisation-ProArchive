"""
image_loader.py — OCR loader for scanned documents (.png, .jpg, .tiff, …)
"""

from pathlib import Path

from ingestion.base import AbstractDocumentLoader
from ingestion.exceptions import IngestionError


class ImageLoader(AbstractDocumentLoader):
    """Run Tesseract OCR on an image file."""

    def load(self, path: Path) -> str:
        try:
            from PIL import Image
            import pytesseract
        except ImportError:
            raise IngestionError("Pillow and pytesseract are required for OCR.")

        try:
            image = Image.open(path)
        except Exception as exc:
            raise IngestionError(f"Failed to open image {path}: {exc}")

        try:
            text = pytesseract.image_to_string(image)
        except Exception as exc:
            raise IngestionError(f"Tesseract OCR failed on {path}: {exc}")

        return text
