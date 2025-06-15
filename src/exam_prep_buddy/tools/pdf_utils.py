from typing import List, Dict
from pathlib import Path
import re
import fitz  # PyMuPDF

def extract_syllabus_modules(pdf_path: str) -> List[str]:
    """
    Extract module names/topics from a syllabus PDF.
    Returns a list of module names or numbers.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    # Simple heuristic: look for lines like 'Module 1:', 'Module 2:', etc.
    modules = re.findall(r"Module\s*\d+[:\-\.]?\s*(.*)", text, re.IGNORECASE)
    if not modules:
        # fallback: split by 'Module' keyword
        modules = re.split(r"Module\s*\d+[:\-\.]?", text, flags=re.IGNORECASE)[1:]
        modules = [m.strip().split('\n')[0] for m in modules]
    return [m.strip() for m in modules if m.strip()]

def categorize_files_by_module(materials_folder: str, modules: List[str]) -> Dict[str, List[str]]:
    """
    Categorize files in the materials folder into modules based on filename/module keywords.
    Returns a dict: {module: [file1, file2, ...]}
    """
    files = [f for f in Path(materials_folder).iterdir() if f.is_file()]
    mapping = {m: [] for m in modules}
    for file in files:
        for module in modules:
            if module.lower().split()[0] in file.name.lower():
                mapping[module].append(str(file))
                break
    return mapping
