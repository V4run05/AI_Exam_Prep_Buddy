#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime
from pathlib import Path

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
    # Example: update these with real values or parse from CLI/GUI
    course_code = "BCSE302L"
    exam_type = "FAT"  # e.g., TH, PR, etc.
    materials_folder_path = r"c:\Varun\VSCode\Projects\LTIMindtree Internship\dbs material"
    current_year = str(datetime.now().year)

    # Locate syllabus PDF
    syllabus_pdf = None
    for file in os.listdir(materials_folder_path):
        if file.lower().endswith('.pdf') and 'syllabus' in file.lower() or course_code in file:
            syllabus_pdf = os.path.join(materials_folder_path, file)
            break
    if not syllabus_pdf:
        # fallback: pick the first PDF
        for file in os.listdir(materials_folder_path):
            if file.lower().endswith('.pdf'):
                syllabus_pdf = os.path.join(materials_folder_path, file)
                break
    if not syllabus_pdf:
        raise FileNotFoundError("No syllabus PDF found in materials folder.")

    # Prepare inputs for the crew
    inputs = {
        'topic': 'Database Systems',
        'course_code': course_code,
        'exam_type': exam_type,
        'materials_folder_path': materials_folder_path,
        'syllabus_pdf': syllabus_pdf
    }

    try:
        buddy = ExamPrepBuddy()
        buddy.set_inputs(inputs)
        buddy.crew().kickoff()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
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
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        ExamPrepBuddy().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
