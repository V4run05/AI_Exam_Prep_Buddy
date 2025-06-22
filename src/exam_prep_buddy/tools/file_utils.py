import os
from .pdf_utils import extract_text_from_pdf
from .docx_utils import extract_text_from_docx
from .pptx_utils import extract_text_from_pptx

def extract_text_from_file(file_path):
    ext = file_path.lower().split('.')[-1]
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext == 'docx':
        return extract_text_from_docx(file_path)
    elif ext == 'pptx':
        return extract_text_from_pptx(file_path)
    elif ext == 'ppt':
        raise ValueError("Old .ppt files are not supported. Please convert your file to .pptx and try again.")
    else:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

def write_text_to_file(filepath, text):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
