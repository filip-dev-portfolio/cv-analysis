from pathlib import Path

from docx import Document
from pypdf import PdfReader


class DocumentParserError(Exception):
    pass


def extract_pdf(path: Path) -> str:
    try:
        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:
            text = page.extract_text() or ""
            pages.append(text)

        return "\n".join(pages).strip()

    except Exception as exc:
        raise DocumentParserError(
            f"Could not read PDF: {path.name}"
        ) from exc


def extract_docx(path: Path) -> str:
    try:
        document = Document(str(path))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs).strip()

    except Exception as exc:
        raise DocumentParserError(
            f"Could not read DOCX: {path.name}"
        ) from exc


def extract_text(path: Path) -> str:
    try:
        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).strip()

    except Exception as exc:
        raise DocumentParserError(
            f"Could not read text file: {path.name}"
        ) from exc


def extract_document(path: Path) -> str:
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return extract_pdf(path)

    if suffix == ".docx":
        return extract_docx(path)

    if suffix in {".txt", ".md"}:
        return extract_text(path)

    raise DocumentParserError(
        f"Unsupported document type: {suffix}"
    )
