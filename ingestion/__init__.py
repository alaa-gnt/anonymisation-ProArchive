"""
ingestion — Document reading layer

Usage:
    from ingestion import read_file, UnsupportedFormatError
"""

from ingestion.reader import read_file
from ingestion.exceptions import UnsupportedFormatError

__all__ = ["read_file", "UnsupportedFormatError"]
