#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from exam_prep_buddy.crew import ExamPrepBuddy
from exam_prep_buddy.tools.file_utils import extract_text_from_file, write_text_to_file

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def chunk_text(text, max_length=2500):
    """
    Split text into chunks of max_length characters, trying to split at paragraph boundaries.
    """
    import re
    paragraphs = re.split(r'(\n\s*\n)', text)
    chunks = []
    current = ''
    for para in paragraphs:
        if len(current) + len(para) < max_length:
            current += para
        else:
            if current:
                chunks.append(current)
            current = para
    if current:
        chunks.append(current)
    return chunks


def extract_headings(text):
    """
    Extract likely section headings from text using simple heuristics:
    - Lines in ALL CAPS
    - Lines starting with numbers (e.g., '1.', '2.1', etc.)
    - Lines with few words (<= 8) and not just stopwords
    """
    import re
    headings = set()
    for line in text.splitlines():
        line_strip = line.strip()
        if not line_strip:
            continue
        # ALL CAPS
        if line_strip.isupper() and len(line_strip) > 3:
            headings.add(line_strip)
            continue
        # Numbered headings
        if re.match(r'^(\d+\.|\d+\s|\d+\.|[IVXLC]+\.|[A-Z]\.)', line_strip):
            headings.add(line_strip)
            continue
        # Short lines (likely headings)
        if 2 <= len(line_strip.split()) <= 8 and not line_strip.endswith('.'):
            headings.add(line_strip)
    return list(headings)


def run():
    """
    Run the crew with chunked input and heading-constrained note generation, then produce a single, well-structured summary.
    """
    # Set your input file path here
    material_file = r"C:\Varun\VSCode\Projects\LTIMindtree Internship\dbs material\module 6_silber.pptx"  # <-- Change this path as needed
    if not os.path.isfile(material_file):
        print(f"File not found: {material_file}")
        return
    print(f"Extracting text from: {material_file}")
    text = extract_text_from_file(material_file)
    print(f"Extracted {len(text)} characters.")

    # Chunk the extracted text
    chunks = chunk_text(text, max_length=2500)
    print(f"Split into {len(chunks)} chunks.")

    # Save chunked text for inspection
    output_dir = os.path.join(os.path.dirname(__file__), '../../output_notes')
    os.makedirs(output_dir, exist_ok=True)
    chunk_file = os.path.join(output_dir, 'extracted_text_chunks.txt')
    with open(chunk_file, 'w', encoding='utf-8') as f:
        for i, chunk in enumerate(chunks):
            f.write(f"\n--- Chunk {i+1} ---\n")
            f.write(chunk)
            f.write("\n")
    print(f"Chunked extracted text written to: {chunk_file}")

    # Collect all headings and all content
    all_headings = set()
    all_content = []
    for chunk in chunks:
        all_content.append(chunk)
        all_headings.update(extract_headings(chunk))
    headings_str = '\n'.join(sorted(all_headings))
    full_content = '\n'.join(all_content)

    # Run CrewAI once on the full content and all headings to generate a single, well-structured summary
    print("Generating final summary notes...")
    inputs = {
        'material_text': full_content,
        'material_file': material_file,
        'allowed_headings': headings_str
    }
    try:
        notes = ExamPrepBuddy().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew for the final summary: {e}")

    out_file = os.path.join(output_dir, 'notes.md')
    write_text_to_file(out_file, notes if isinstance(notes, str) else str(notes))
    print(f"Final summary notes written to: {out_file}")


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
