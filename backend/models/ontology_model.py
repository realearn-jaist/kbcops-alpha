import os
from flask import current_app # type: ignore

from utils.file_handler import load_file, replace_or_create_folder, save_file

def save_ontology(file, id, filename):
    STORAGE_FOLDER = current_app.config['STORAGE_FOLDER']
    path = os.path.join(STORAGE_FOLDER, id)
    
    replace_or_create_folder(path)
    
    path = os.path.join(path, filename)
    
    return save_file(file, path)

def list_ontology():
    STORAGE_FOLDER = current_app.config['STORAGE_FOLDER']
    
    ontologies = []
    
    for dirname in os.listdir(STORAGE_FOLDER):
        dirpath = os.path.join(STORAGE_FOLDER, dirname)
        if os.path.isdir(dirpath):
            ontologies.append(dirname)
        
    return ontologies

def getPath_ontology(id):
    try:
        filename = id + '.owl'
        STORAGE_FOLDER = current_app.config['STORAGE_FOLDER']
        path = os.path.join(STORAGE_FOLDER, id, filename)
        
        return path
    except FileNotFoundError:
        return None

