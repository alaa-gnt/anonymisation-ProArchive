"""
base.py — Abstract document loader
"""

from abc import ABC, abstractmethod
from pathlib import Path


class AbstractDocumentLoader(ABC):
    """Every file-type loader inherits from this class."""

    @abstractmethod
    def load(self, path: Path) -> str:
        """
        Extract raw text from the given file.

        Parameters
        ----------
        path : Path
            Absolute or relative path to the document.

        Returns
        -------
        str
            The full text content of the document.

        Raises
        ------
        IngestionError
            On any read / decode / OCR failure.
        """
