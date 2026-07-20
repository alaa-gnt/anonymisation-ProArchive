from pathlib import Path

from ingestion.base import AbstractDocumentLoader
from ingestion.document import StructuredDocument, TextBlock
from ingestion.exceptions import IngestionError


class PdfLoader(AbstractDocumentLoader):
    def load(self, path: Path) -> StructuredDocument:
        try:
            import fitz
        except ImportError:
            raise IngestionError("PyMuPDF (fitz) is required to read PDFs.")

        try:
            doc = fitz.open(path)
        except Exception as exc:
            raise IngestionError(f"Failed to open PDF {path}: {exc}")

        blocks = []
        pages_text = []

        for page_num, page in enumerate(doc, 1):
            pages_text.append(page.get_text())

            for b in page.get_text("blocks"):
                x0, y0, x1, y1, text, *_ = b
                text = text.strip()
                if not text:
                    continue
                blocks.append(
                    TextBlock(
                        text=text,
                        page=page_num,
                        bbox=(x0, y0, x1, y1),
                        block_type="text",
                    )
                )

        doc.close()

        return StructuredDocument(
            text="\f".join(pages_text),
            blocks=blocks,
            metadata={"pages": len(pages_text)},
        )
