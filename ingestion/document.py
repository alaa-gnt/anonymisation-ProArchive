from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TextBlock:
    text: str
    page: int = 0
    bbox: Optional[tuple[float, float, float, float]] = None
    block_type: str = "text"


@dataclass
class StructuredDocument:
    text: str
    blocks: list[TextBlock]
    metadata: dict
