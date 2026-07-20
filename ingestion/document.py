# the dataclasses that every loader must use 

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TextBlock:
    text: str # the actual string content
    page: int = 0 # which page it's on
    bbox: Optional[tuple[float, float, float, float]] = None # x0, y0, x1, y1 coordinates of the block
    block_type: str = "text" # the type of block, default is "text"


# this is what every .load() returns 
@dataclass 
class StructuredDocument:
    text: str # the actual string content
    blocks: list[TextBlock] # list of text blocks
    metadata: dict # additional metadata about the document
