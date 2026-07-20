from pathlib import Path

from ingestion.base import AbstractDocumentLoader
from ingestion.document import StructuredDocument, TextBlock
from ingestion.exceptions import IngestionError


class ImageLoader(AbstractDocumentLoader):
    def load(self, path: Path) -> StructuredDocument:
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
            data = pytesseract.image_to_data(
                image, lang="ara+fra+eng", output_type=pytesseract.Output.DICT
            )
        except Exception as exc:
            raise IngestionError(f"Tesseract OCR failed on {path}: {exc}")

        blocks = []
        lines = []
        current_line_text = []
        current_line_bbox = None
        current_page = 1
        n = len(data["level"])

        for i in range(n):
            if data["level"][i] == 4:
                if current_line_text:
                    text = " ".join(current_line_text)
                    lines.append(text)
                    if current_line_bbox:
                        blocks.append(
                            TextBlock(
                                text=text,
                                page=current_page,
                                bbox=current_line_bbox,
                                block_type="text",
                            )
                        )
                    current_line_text = []
                    current_line_bbox = None

                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]
                current_line_bbox = (x, y, x + w, y + h)

            if data["level"][i] == 5:
                word = data["text"][i]
                if word.strip():
                    current_line_text.append(word)

        if current_line_text:
            text = " ".join(current_line_text)
            lines.append(text)
            if current_line_bbox:
                blocks.append(
                    TextBlock(text=text, page=current_page, bbox=current_line_bbox, block_type="text")
                )

        full_text = "\n".join(lines)

        return StructuredDocument(
            text=full_text,
            blocks=blocks,
            metadata={"lines": len(lines)},
        )
