import os
from flask import current_app  # type: ignore
import csv
from datetime import datetime

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

def write_to_ownership_csv(alias, ontology_name):
    directory_path = current_app.config["STORAGE_FOLDER"]
    csv_file = os.path.join(directory_path, "ownership.csv")

    # Check if CSV file exists; create headers if it doesn't
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ontology_name', 'alias' ])

    # Append new data to CSV file
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ontology_name, alias])
        
def remove_row_ownership_csv(ontology_name):
    directory_path = current_app.config["STORAGE_FOLDER"]
    csv_file = os.path.join(directory_path, "ownership.csv")
    temp_file = os.path.join(directory_path, "temp_ownership.csv")

    # Open the original CSV file and create a temporary file for writing
    with open(csv_file, mode='r', newline='') as infile, \
         open(temp_file, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write headers to the temporary file
        headers = next(reader)
        writer.writerow(headers)

        # Iterate over rows in the original CSV file
        for row in reader:
            if row[0] != ontology_name:  # Check if ontology_name matches
                writer.writerow(row)

    # Replace the original file with the temporary file
    os.remove(csv_file)
    os.rename(temp_file, csv_file)