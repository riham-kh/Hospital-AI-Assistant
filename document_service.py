
from pypdf import PdfReader


def extract_pdf_pages(file):
    reader = PdfReader(file)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "page_number": page_number,
                "content": text
            })

    return pages


def split_text(text: str, chunk_size: int = 800):
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        if current_chunk and len(current_chunk) + len(word) + 1 > chunk_size:
            chunks.append(current_chunk)
            current_chunk = ""

        current_chunk = f"{current_chunk} {word}".strip()

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
