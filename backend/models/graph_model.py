import base64
import os

from utils.directory_utils import get_path
from utils.exceptions import FileException


import os

def load_graph(ontology_name, algorithm, classifier):
    """Load graph DOT files from directory

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        classifier (str): The name of the classifier
    Returns:
        list: The list of graph DOT file contents
    """
    try:
        directory = get_path(ontology_name, algorithm, classifier, "graph_fig")  # where graph fig save

        dot_files = []

        if not os.path.exists(directory):
            raise FileException(f"Directory '{directory}' does not exist.")

        for filename in os.listdir(directory):
            if filename.endswith(".dot"):
                dot_file_path = os.path.join(directory, filename)
                try:
                    with open(dot_file_path, "r") as dot_file:
                        dot_data = dot_file.read()
                        dot_files.append({"dot_file": dot_data})
                except Exception as e:
                    raise FileException(f"Error reading DOT file '{dot_file_path}': {str(e)}")

        return dot_files

    except FileException:
        raise
    except Exception as e:
        raise FileException(f"Unexpected error loading DOT files: {str(e)}")
