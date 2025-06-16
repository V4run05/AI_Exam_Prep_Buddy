import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file using PyMuPDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text
