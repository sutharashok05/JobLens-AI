from pathlib import Path

from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF resume.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Resume file not found")

    reader = PdfReader(str(path))

    pages_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages_text.append(text)

    extracted_text = "\n".join(pages_text).strip()

    return extracted_text