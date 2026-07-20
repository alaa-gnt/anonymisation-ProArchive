
from pathlib import Path # to read the path

from ingestion.exceptions import UnsupportedFormatError # exception for unsupported file formats
from ingestion.loaders import LOADERS # import the loaders for different file formats


def read_file(path):
    path = Path(path) #read the path as a Path object
    ext = path.suffix.lower() # file extension in lower case 

    loader = LOADERS.get(ext)

    #cheking if the file actually exists or no 
    if loader is None:
        raise UnsupportedFormatError(
            f"Unsupported file extension '{ext}'. "
            f"Supported: {', '.join(sorted(LOADERS.keys()))}"
        )

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    doc = loader.load(path)

    metadata = {
        "source": str(path.resolve()),
        "extension": ext,
        "filename": path.name,
        "char_count": len(doc.text),
        **doc.metadata,
    }

    return doc.text, metadata
