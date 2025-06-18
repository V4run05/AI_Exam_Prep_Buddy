import os
import re

def categorize_materials_by_filename(folder_path, module_topics, textbook_keywords):
    """
    Categorize files in the given folder based on provided module_topics and textbook_keywords.
    Args:
        folder_path (str): Path to the materials folder.
        module_topics (dict): Dict of module names to list of topic keywords.
        textbook_keywords (list): List of keywords to identify textbooks/references.
    Returns:
        dict: Mapping of module/topic to list of file paths.
    """
    categorized = {m: [] for m in module_topics}
    categorized['Textbooks'] = []
    categorized['Others'] = []

    def is_explicit_module_folder(folder_name):
        lower = folder_name.lower()
        for module in module_topics:
            mod_num = module.split()[-1]
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
            if any(key in lower_fname for key in textbook_keywords):
                categorized['Textbooks'].append(os.path.relpath(fpath, folder_path))
                continue
            # Module number and topic detection
            module_found = False
            for module, topics in module_topics.items():
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
