import csv
import json
import os
import pandas as pd

from utils.directory_utils import get_path
from utils.exceptions import FileException


def write_evaluate(ontology_name: str, algorithm: str, classifier: str, data: dict):
    """Writes the evaluation data to a json file

    Args:
        ontology (str): The name of the ontology
        algorithm (str): The name of the algorithm
        classifier (str): The name of the classifier
        data (dict): The evaluation data
    Returns:
        None
    """
    try:
        file_path = get_path(ontology_name, algorithm, classifier, "performance.json")
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        raise FileException(f"Error writing evaluation data: {str(e)}")


def read_evaluate(ontology_name: str, algorithm: str, classifier: str):
    """Reads the evaluation data from a json file

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        classifier (str): The name of the classifier
    Returns:
        dict: The evaluation data
    """
    try:
        file_path = get_path(ontology_name, algorithm, classifier, "performance.json")
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        raise FileException(f"Evaluation file not found: {file_path}", 404)
    except Exception as e:
        raise FileException(f"Error reading evaluation data: {str(e)}")


def write_garbage_metrics(
    ontology_name: str, algorithm: str, classifier: str, data: list
):
    """Writes the garbage metrics data to a csv file

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        classifier (str): The name of the classifier
        data (list): The garbage metrics data
    Returns:
        list: The garbage metrics data
    """
    try:
        json_output = []
        file_path = get_path(ontology_name, algorithm, classifier, "garbage.csv")
        with open(file_path, "w", newline="") as csv_file:
            column_names = list(data[0].keys())
            csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
            csv_writer.writeheader()
            csv_writer.writerows(data)
        return json_output
    except Exception as e:
        raise FileException(f"Error writing garbage metrics: {str(e)}")


def read_garbage_metrics(ontology_name: str, algorithm: str, classifier: str):
    """Reads the garbage metrics data from a csv file

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        classifier (str): The name of the classifier
    Returns:
        list: The garbage metrics data
    """
    try:
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
        file_path = get_path(ontology_name, algorithm, classifier, "garbage.csv")
        with open(file_path, mode="r", newline="") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                row_dict = {headers[i]: row[i] for i in range(len(headers))}
                json_output.append(row_dict)
        return json_output
    except FileNotFoundError:
        raise FileException(f"Garbage metrics file not found: {file_path}", 404)
    except Exception as e:
        raise FileException(f"Error reading garbage metrics: {str(e)}")


def read_garbage_metrics_pd(ontology_name: str, algorithm: str, classifier: str):
    """Reads the garbage metrics data from a csv file

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        classifier (str): The name of the classifier
    Returns:
        pd.DataFrame: The garbage metrics data
    """
    try:
        file_path = get_path(ontology_name, algorithm, classifier, "garbage.csv")
        garbage_file = pd.read_csv(file_path)
        return garbage_file
    except FileNotFoundError:
        raise FileException(f"Garbage metrics file not found: {file_path}", 404)
    except Exception as e:
        raise FileException(f"Error reading garbage metrics with pandas: {str(e)}")
