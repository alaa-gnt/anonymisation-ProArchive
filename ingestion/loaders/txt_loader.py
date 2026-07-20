from pathlib import Path

from ingestion.base import AbstractDocumentLoader
from ingestion.document import StructuredDocument, TextBlock
from ingestion.exceptions import IngestionError


class TxtLoader(AbstractDocumentLoader):
    ENCODINGS = ["utf-8", "latin-1", "windows-1256"]

    def load(self, path: Path) -> StructuredDocument:
        for enc in self.ENCODINGS:
            try:
                with open(path, "r", encoding=enc) as f:
                    raw = f.read()
            except UnicodeDecodeError:
                continue

        if not raw:
            raise IngestionError(f"Could not decode {path} with any known encoding.")

        lines = raw.splitlines(keepends=True)
        blocks = []
        for i, line in enumerate(lines):
            blocks.append(TextBlock(text=line, page=0, block_type="text"))

        return StructuredDocument(
            text=raw,
            blocks=blocks,
            metadata={"encoding": enc},
        )
