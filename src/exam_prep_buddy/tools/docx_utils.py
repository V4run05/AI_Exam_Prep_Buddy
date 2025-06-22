from docx import Document

def extract_text_from_docx(docx_path):
    """Extract all text from a DOCX file."""
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
