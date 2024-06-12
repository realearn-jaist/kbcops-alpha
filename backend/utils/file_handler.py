import os
import shutil

def replace_or_create_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        
    os.makedirs(folder_path)
    return folder_path
    
def save_file(file, path):
    try:
        file.save(path)
        return path
    except Exception as e:
        print(f"Error saving file: {e}")
        return None
    
def load_file(path):
    if os.path.isfile(path):
        with open(path) as onto_file:
            return onto_file
    else:
        raise FileNotFoundError