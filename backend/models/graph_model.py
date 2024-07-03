import base64
import os

from utils.directory_utils import get_path
from utils.exceptions import FileException


def load_graph(ontology_name, algorithm, classifier):
    """Load graph fig from directory

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        classifier (str): The name of the classifier
    Returns:
        list: The list of graph figures
    """
    try:
        directory = get_path(ontology_name, algorithm, classifier, "graph_fig")  # where graph fig save

        images = []

        if not os.path.exists(directory):
            raise FileException(f"Directory '{directory}' does not exist.")

        for _, filename in enumerate(os.listdir(directory)):
            if (
                filename.endswith(".png")
                or filename.endswith(".jpg")
                or filename.endswith(".jpeg")
            ):
                image_path = os.path.join(directory, filename)
                try:
                    with open(image_path, "rb") as img_file:
                        img_data = img_file.read()
                        img_base64 = base64.b64encode(img_data).decode("utf-8")
                        images.append({"image": img_base64})
                except Exception as e:
                    raise FileException(f"Error reading image file '{image_path}': {str(e)}")

        return images

    except FileException:
        raise
    except Exception as e:
        raise FileException(f"Unexpected error loading graph images: {str(e)}")
