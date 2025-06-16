import os
from .pdf_utils import extract_text_from_pdf
from .docx_utils import extract_text_from_docx
from .pptx_utils import extract_text_from_pptx

def extract_all_materials(folder_path):
    extracted = {}
    if folder_path and os.path.isdir(folder_path):
        for fname in os.listdir(folder_path):
            fpath = os.path.join(folder_path, fname)
            if fname.lower().endswith('.pdf'):
                extracted[fname] = extract_text_from_pdf(fpath)
            elif fname.lower().endswith('.docx'):
                extracted[fname] = extract_text_from_docx(fpath)
            elif fname.lower().endswith('.pptx'):
                extracted[fname] = extract_text_from_pptx(fpath)
    return extracted
