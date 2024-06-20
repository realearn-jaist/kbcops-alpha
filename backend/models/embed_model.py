import os
import joblib
import gensim
import numpy

from models.extract_model import load_classes
from utils.file_handler import replace_or_create_folder
from models.ontology_model import getPath_ontology, getPath_ontology_directory


def isModelExist(ontology_name, algorithm):
    """Check if the model exists in the directory
    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        bool: True if the model exists, False otherwise"""
    path = os.path.join(getPath_ontology_directory(ontology_name), algorithm, "model")

    return os.path.exists(path)


def save_model(ontology_name, algorithm, model):
    """Save the model to the directory
    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        model (object): The model to save

    Returns:
        None
    """
    path = os.path.join(getPath_ontology_directory(ontology_name), algorithm)

    replace_or_create_folder(path)

    path = os.path.join(path, "model")
    if algorithm == "rdf2vec":
        joblib.dump(model, path)
    else:
        model.save(path)


def load_model(ontology_name, algorithm):
    """Load the model from the directory
    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        object: The model"""
    if not isModelExist(ontology_name, algorithm):
        return None

    path = os.path.join(getPath_ontology_directory(ontology_name), algorithm, "model")

    if algorithm == "rdf2vec":
        return joblib.load(path)
    else:
        return gensim.models.word2vec.Word2Vec.load(path)


def save_embedding(ontology_name, algorithm, embed):
    """Save the embedding to the directory
    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        embed (numpy.ndarray): The embedding to save
    Returns:
        numpy.ndarray: The embedding saved"""
    if not isModelExist(ontology_name, algorithm):
        return None

    path = os.path.join(
        getPath_ontology_directory(ontology_name), algorithm, "embeddings.npy"
    )

    numpy.save(path, embed)

    return embed


def load_embedding(ontology_name, algorithm):
    """Load the embedding from the directory
    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        numpy.ndarray: The embedding saved"""
    no_class = len(load_classes(ontology_name))

    if not isModelExist(ontology_name, algorithm):
        return None

    path = os.path.join(
        getPath_ontology_directory(ontology_name), algorithm, "embeddings.npy"
    )

    with open(path, "rb") as f:
        embedding = numpy.load(f)
        return embedding[:no_class], embedding[no_class:]
