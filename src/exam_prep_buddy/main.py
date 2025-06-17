#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from exam_prep_buddy.tools.pdf_utils import extract_text_from_pdf
from exam_prep_buddy.tools.material_utils import extract_all_materials
from exam_prep_buddy.tools.categorize_utils import categorize_materials_by_filename

from exam_prep_buddy.crew import ExamPrepBuddy

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

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
    categorized_materials = categorize_materials_by_filename(materials_folder_path)
    inputs = {
        'syllabus_pdf': syllabus_pdf_path,
        'materials_folder': materials_folder_path,
        'syllabus_text': syllabus_text,
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
