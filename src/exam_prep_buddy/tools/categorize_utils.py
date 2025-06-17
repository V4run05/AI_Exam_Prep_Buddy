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

    def is_explicit_module_folder(folder_name):
        lower = folder_name.lower()
        for module in MODULE_TOPICS:
            mod_num = module.split()[-1]
            # Accepts: module 3, mod3, mod 3, m3, etc.
            if re.fullmatch(rf"(module|mod|m)[ _-]*{mod_num}(\b|[^a-z0-9].*)?", lower):
                return module
        return None

    def process_folder(current_path, force_module=None):
        for fname in os.listdir(current_path):
            fpath = os.path.join(current_path, fname)
            lower_fname = fname.lower()
            if os.path.isdir(fpath):
                module_for_folder = is_explicit_module_folder(fname)
                if force_module or module_for_folder:
                    # Assign all files (recursively) in this folder to the module
                    module = force_module or module_for_folder
                    for root, _, files in os.walk(fpath):
                        for subfile in files:
                            subfile_path = os.path.join(root, subfile)
                            categorized[module].append(os.path.relpath(subfile_path, folder_path))
                else:
                    process_folder(fpath)
                continue
            # Only process files
            # Textbook/Reference detection
            if any(key in lower_fname for key in TEXTBOOK_KEYWORDS):
                categorized['Textbooks'].append(os.path.relpath(fpath, folder_path))
                continue
            # Module number and topic detection
            module_found = False
            for module, topics in MODULE_TOPICS.items():
                mod_num = module.split()[-1]
                if re.search(rf"\\b(module|mod|m)[ _-]*{mod_num}(\\b|[^a-z0-9].*)?", lower_fname):
                    categorized[module].append(os.path.relpath(fpath, folder_path))
                    module_found = True
                    break
                for topic in topics:
                    if topic in lower_fname:
                        categorized[module].append(os.path.relpath(fpath, folder_path))
                        module_found = True
                        break
                if module_found:
                    break
            if not module_found:
                categorized['Others'].append(os.path.relpath(fpath, folder_path))

    if folder_path and os.path.isdir(folder_path):
        process_folder(folder_path)
    return categorized
