#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from exam_prep_buddy.tools.pdf_utils import extract_text_from_pdf
from exam_prep_buddy.tools.material_utils import extract_all_materials
from exam_prep_buddy.tools.categorize_utils import categorize_materials_by_filename
from exam_prep_buddy.crew import ExamPrepBuddy
import re

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def extract_module_topics_and_keywords(syllabus_text):
    """
    Dummy parser: Extracts modules and topics from syllabus text using regex.
    You should replace this with your CrewAI agent call for production.
    Returns (module_topics, textbook_keywords)
    """
    module_topics = {}
    textbook_keywords = set()
    module_pattern = re.compile(r"Module\s*(\d+)[\s:.-]*(.*?)(?=Module\s*\d+|$)", re.IGNORECASE | re.DOTALL)
    for match in module_pattern.finditer(syllabus_text):
        module_num = match.group(1)
        module_content = match.group(2).strip()
        topics = re.findall(r"[\w\- ]+", module_content)
        topics = [t.strip().lower() for t in topics if t.strip()]
        module_topics[f"Module {module_num}"] = topics
        textbook_keywords.update([t for t in topics if any(k in t for k in ["textbook", "reference", "fundamental", "introduction", "dbms", "database"])])
    # Add some generic textbook keywords
    textbook_keywords.update(["textbook", "reference", "fundamental", "introduction", "dbms", "database"])
    return module_topics, list(textbook_keywords)

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew with all required exam prep inputs.
    """
    syllabus_pdf_path = r"C:\Varun\VSCode\Projects\LTIMindtree Internship\BCSE302L_DATABASE-SYSTEMS_TH_1.0_67_BCSE302L.pdf"
    materials_folder_path = r"C:\Varun\VSCode\Projects\LTIMindtree Internship\dbs material"
    syllabus_text = extract_text_from_pdf(syllabus_pdf_path)
    module_topics, textbook_keywords = extract_module_topics_and_keywords(syllabus_text)
    categorized_materials = categorize_materials_by_filename(materials_folder_path, module_topics, textbook_keywords)
    inputs = {
        'syllabus_pdf': syllabus_pdf_path,
        'materials_folder': materials_folder_path,
        'syllabus_text': syllabus_text,
        'module_topics': module_topics,
        'textbook_keywords': textbook_keywords,
        'categorized_materials': categorized_materials
    }
    try:
        ExamPrepBuddy().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'syllabus_pdf': "C:\Varun\VSCode\Projects\LTIMindtree Internship\BCSE302L_DATABASE-SYSTEMS_TH_1.0_67_BCSE302L.pdf",
        'materials_folder': "C:\Varun\VSCode\Projects\LTIMindtree Internship\dbs material",
    }
    try:
        ExamPrepBuddy().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ExamPrepBuddy().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'syllabus_pdf': "C:\Varun\VSCode\Projects\LTIMindtree Internship\BCSE302L_DATABASE-SYSTEMS_TH_1.0_67_BCSE302L.pdf",
        'materials_folder': "C:\Varun\VSCode\Projects\LTIMindtree Internship\dbs material",
    }
    
    try:
        ExamPrepBuddy().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
