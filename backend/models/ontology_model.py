import os
from flask import current_app
import csv
from utils.directory_utils import replace_or_create_folder
from utils.exceptions import FileException


def save_ontology(file, ontology_name, filename):
    """Save the ontology file to the storage folder

    Args:
        file (FileStorage): The ontology file
        ontology_name (str): The name of the ontology
        filename (str): The name of the file
    Returns:
        str: The path of the saved file
    """
    try:
        STORAGE_FOLDER = current_app.config["STORAGE_FOLDER"]
        path = os.path.join(STORAGE_FOLDER, ontology_name)

        replace_or_create_folder(path)

        path = os.path.join(path, filename)

        file.save(path)
        return path
    except Exception as e:
        raise FileException(f"Error saving ontology: {str(e)}")


def list_ontology():
    """List all the ontologies in the storage folder

    Returns:
        list: The list of ontologies
    """
    try:
        STORAGE_FOLDER = current_app.config["STORAGE_FOLDER"]

        ontologies = []

        for dirname in os.listdir(STORAGE_FOLDER):
            dirpath = os.path.join(STORAGE_FOLDER, dirname)
            if os.path.isdir(dirpath):
                ontologies.append(dirname)

        return ontologies
    except Exception as e:
        raise FileException(f"Error listing ontologies: {str(e)}")


def write_to_ownership_csv(alias, ontology_name):
    """Write ontology ownership data to a CSV file

    Args:
        alias (str): The alias of the user
        ontology_name (str): The name of the ontology
    Returns:
        None
    """
    try:
        directory_path = current_app.config["STORAGE_FOLDER"]
        csv_file = os.path.join(directory_path, "ownership.csv")

        # Check if CSV file exists; create headers if it doesn't
        if not os.path.exists(csv_file):
            with open(csv_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ontology_name", "alias"])

        # Append new data to CSV file
        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([ontology_name, alias])
    except Exception as e:
        raise FileException(f"Error writing to CSV file: {str(e)}")


def remove_row_ownership_csv(ontology_name):
    """Remove a row from the ownership CSV file

    Args:
        ontology_name (str): The name of the ontology
    Returns:
        None
    """
    try:
        directory_path = current_app.config["STORAGE_FOLDER"]
        csv_file = os.path.join(directory_path, "ownership.csv")
        temp_file = os.path.join(directory_path, "temp_ownership.csv")

        # Open the original CSV file and create a temporary file for writing
        with open(csv_file, mode="r", newline="") as infile, open(
            temp_file, mode="w", newline=""
        ) as outfile:
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
    except Exception as e:
        raise FileException(f"Error removing row from CSV file: {str(e)}")
