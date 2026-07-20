

class IngestionError(Exception):
    """Base exception for all ingestion-layer errors."""


class UnsupportedFormatError(IngestionError):
    """Raised when the file extension has no registered loader."""
