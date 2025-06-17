import os
import re

MODULE_TOPICS = {
    'Module 1': ['architecture', 'introduction', 'data model', 'dbms', 'database system', 'schema', 'three-schema', 'abstraction'],
    'Module 2': ['er model', 'entity relationship', 'attributes', 'relationships', 'e-r', 'eer', 'enhanced er'],
    'Module 3': ['relational model', 'relational algebra', 'relational calculus', 'keys', 'constraints', 'normalization'],
    'Module 4': ['sql', 'queries', 'subqueries', 'views', 'triggers', 'procedures'],
    'Module 5': ['transactions', 'concurrency', 'recovery', 'serializability', 'locking', 'deadlock'],
    'Module 6': ['indexing', 'hashing', 'storage', 'file organization', 'b-trees', 'query optimization'],
    'Module 7': ['nosql', 'big data', 'column store', 'document store', 'graph db', 'cap theorem'],
}

TEXTBOOK_KEYWORDS = [
    'textbook', 'reference', 'elmasri', 'navathe', 'silberschatz', 'database-system-concepts', 'fundamentals', 'introduction to database', 'dbms', 'database concepts'
]

def categorize_materials_by_filename(folder_path):
    categorized = {m: [] for m in MODULE_TOPICS}
    categorized['Textbooks'] = []
    categorized['Others'] = []
    if folder_path and os.path.isdir(folder_path):
        for fname in os.listdir(folder_path):
            lower_fname = fname.lower()
            # Textbook/Reference detection
            if any(key in lower_fname for key in TEXTBOOK_KEYWORDS):
                categorized['Textbooks'].append(fname)
                continue
            # Module number detection
            module_found = False
            for module, topics in MODULE_TOPICS.items():
                # Match 'module 3', 'mod3', 'mod 3', etc.
                if re.search(rf"\\b{module.lower().replace('module ', 'module ?')}\\b", lower_fname) or re.search(rf"\\bmod ?{module[-1]}\\b", lower_fname):
                    categorized[module].append(fname)
                    module_found = True
                    break
                # Topic detection
                for topic in topics:
                    if topic in lower_fname:
                        categorized[module].append(fname)
                        module_found = True
                        break
                if module_found:
                    break
            if not module_found:
                categorized['Others'].append(fname)
    return categorized
