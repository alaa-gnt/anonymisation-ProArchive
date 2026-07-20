# loading different file formats using their respective loaders

from ingestion.loaders.txt_loader import TxtLoader
from ingestion.loaders.pdf_loader import PdfLoader
from ingestion.loaders.docx_loader import DocxLoader
from ingestion.loaders.image_loader import ImageLoader


# Maps file extension → loader instance.
# Add a new entry here when a new loader is written.
LOADERS = {
    ".txt": TxtLoader(),
    ".md": TxtLoader(),
    ".csv": TxtLoader(),
    ".json": TxtLoader(),
    ".xml": TxtLoader(),
    ".html": TxtLoader(),
    ".pdf": PdfLoader(),
    ".docx": DocxLoader(),
    ".png": ImageLoader(),
    ".jpg": ImageLoader(),
    ".jpeg": ImageLoader(),
    ".tiff": ImageLoader(),
    ".tif": ImageLoader(),
}
