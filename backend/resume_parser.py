import pdfplumber
from docx import Document
import os

def parse_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def parse_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        if para.text:
            text.append(para.text)
    return "\n".join(text).strip()


def extract_resume_text(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError("Resume file not found")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext == ".docx":
        return parse_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX are allowed.")
