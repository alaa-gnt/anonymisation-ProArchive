from abc import ABC, abstractmethod
from pathlib import Path

from ingestion.document import StructuredDocument


class AbstractDocumentLoader(ABC):
    # every loader must implement this method to load a document from a given path
    @abstractmethod
    def load(self, path: Path) -> StructuredDocument:
        pass
