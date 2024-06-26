import base64
import os

from models.ontology_model import get_path_ontology_directory


def load_graph(ontology_name, algorithm, classifier):
    """Load graph fig from directory

    Args:
        onto (str): The name of the ontology
        algo (str): The name of the algorithm
    Returns:
        list: The list of graph fig
    """
    directory = os.path.join(
        get_path_ontology_directory(ontology_name), algorithm, classifier, "graph_fig"
    )  # where graph fig save

    images = []

    if not os.path.exists(directory):
        raise ValueError(f"Directory '{directory}' does not exist.")

    for _, filename in enumerate(os.listdir(directory)):
        if (
            filename.endswith(".png")
            or filename.endswith(".jpg")
            or filename.endswith(".jpeg")
        ):
            image_path = os.path.join(directory, filename)
            with open(image_path, "rb") as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode("utf-8")
                images.append({"image": img_base64})

    return images
