import csv
import json
import os

import pandas as pd

from models.ontology_model import get_path_ontology_directory


def write_evaluate(ontology, algorithm, data):
    """Writes the evaluation data to a json file

    Args:
        ontology (str): The name of the ontology
        algorithm (str): The name of the algorithm
        data (dict): The evaluation data
    Returns:
        None
    """
    file_path = os.path.join(
        get_path_ontology_directory(ontology), algorithm, "performance.json"
    )

    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def read_evaluate(ontology, algorithm):
    """Reads the evaluation data from a json file

    Args:
        ontology (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        dict: The evaluation data
    """
    file_path = os.path.join(
        get_path_ontology_directory(ontology), algorithm, "performance.json"
    )

    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def write_garbage_metrics(ontology, algorithm, data):
    """Writes the garbage metrics data to a csv file

    Args:
        ontology (str): The name of the ontology
        algorithm (str): The name of the algorithm
        data (list): The garbage metrics data
    Returns:
        None
    """
    json_output = []

    file_path = os.path.join(
        get_path_ontology_directory(ontology), algorithm, "garbage.csv"
    )

    with open(file_path, "w", newline="") as csv_file:
        column_names = list(data[0].keys())
        csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
        csv_writer.writeheader()
        csv_writer.writerows(data)

    return json_output


def read_garbage_metrics(ontology, algorithm):
    """Reads the garbage metrics data from a csv file

    Args:
        ontology (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        list: The garbage metrics data
    """
    json_output = []

    headers = [
        "Individual",
        "Predicted",
        "Predicted_rank",
        "True",
        "True_rank",
        "Score_predict",
        "Score_true",
        "Dif",
    ]

    file_path = os.path.join(
        get_path_ontology_directory(ontology), algorithm, "garbage.csv"
    )

    with open(file_path, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            row_dict = {headers[i]: row[i] for i in range(len(headers))}
            json_output.append(row_dict)

    return json_output


def read_garbage_metrics_pd(ontology, algorithm):
    """Reads the garbage metrics data from a csv file

    Args:
        ontology (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        pd.DataFrame: The garbage metrics data
    """
    file_path = os.path.join(
        get_path_ontology_directory(ontology), algorithm, "garbage.csv"
    )

    garbage_file = pd.read_csv(file_path)

    return garbage_file
