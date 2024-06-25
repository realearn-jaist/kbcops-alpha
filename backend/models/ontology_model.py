import os
from flask import current_app  # type: ignore

from utils.file_handler import replace_or_create_folder, save_file


def save_ontology(file, ontology_name, filename):
    """Save the ontology file to the storage folder

    Args:
        file (FileStorage): The ontology file
        id (str): The id of the ontology
        filename (str): The name of the file
    Returns:
        str: The path of the saved file
    """
    STORAGE_FOLDER = current_app.config["STORAGE_FOLDER"]
    path = os.path.join(STORAGE_FOLDER, ontology_name)

    replace_or_create_folder(path)

    path = os.path.join(path, filename)

    return save_file(file, path)


def list_ontology():
    """List all the ontologies in the storage folder

    Returns:
        list: The list of ontologies
    """
    STORAGE_FOLDER = current_app.config["STORAGE_FOLDER"]

    ontologies = []

    for dirname in os.listdir(STORAGE_FOLDER):
        dirpath = os.path.join(STORAGE_FOLDER, dirname)
        if os.path.isdir(dirpath):
            ontologies.append(dirname)

    return ontologies


def get_path_ontology(ontology_name):
    """Get the path of the ontology file

    Args:
        id (str): The id of the ontology
    Returns:
        str: The path of the ontology file
    """
    try:
        filename = ontology_name + ".owl"
        STORAGE_FOLDER = current_app.config["STORAGE_FOLDER"]
        path = os.path.join(STORAGE_FOLDER, ontology_name, filename)

        return path
    except FileNotFoundError:
        return None


def get_path_ontology_directory(ontology_name):
    """Get the path of the ontology directory

    Args:
        id (str): The id of the ontology
    Returns:
        str: The path of the ontology directory
    """
    try:
        STORAGE_FOLDER = current_app.config["STORAGE_FOLDER"]
        path = os.path.join(STORAGE_FOLDER, ontology_name)

        return path
    except FileNotFoundError:
        return None
