import os
import joblib
import gensim
import numpy

from models.extract_model import load_multi_input_files
from utils.directory_utils import get_path, replace_or_create_folder
from utils.exceptions import FileException


def isModelExist(ontology_name, algorithm):
    """Check if the model exists in the directory

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        bool: True if the model exists, False otherwise
    """
    try:
        path = get_path(ontology_name, algorithm, "model")
        return os.path.exists(path)
    except Exception as e:
        raise FileException(f"Error checking if model exists: {str(e)}")


def save_model(ontology_name, algorithm, model):
    """Save the model to the directory

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        model (object): The model to save

    Returns:
        None
    """
    try:
        path = get_path(ontology_name, algorithm)
        replace_or_create_folder(path)
        path = os.path.join(path, "model")
        if algorithm == "rdf2vec":
            joblib.dump(model, path)
        else:
            model.save(path)
    except Exception as e:
        raise FileException(f"Error saving model: {str(e)}")


def load_model(ontology_name, algorithm):
    """Load the model from the directory

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        object: The model
    """
    try:
        if not isModelExist(ontology_name, algorithm):
            return None
        path = get_path(ontology_name, algorithm, "model")
        if algorithm == "rdf2vec":
            return joblib.load(path)
        else:
            return gensim.models.word2vec.Word2Vec.load(path)
    except Exception as e:
        raise FileException(f"Error loading model: {str(e)}")


def save_embedding(ontology_name, algorithm, embed):
    """Save the embedding to the directory

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        embed (numpy.ndarray): The embedding to save
    Returns:
        numpy.ndarray: The embedding saved
    """
    try:
        if not isModelExist(ontology_name, algorithm):
            return None
        path = get_path(ontology_name, algorithm, "embeddings.npy")
        numpy.save(path, embed)
        return embed
    except Exception as e:
        raise FileException(f"Error saving embedding: {str(e)}")


def load_embedding_value(ontology_name: str, algorithm: str):
    """Load the embedding from the directory

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        numpy.ndarray: The embedding loaded
    """
    try:
        no_class = len(load_multi_input_files(ontology_name, ["classes"])["classes"])
        if not isModelExist(ontology_name, algorithm):
            return None
        path = get_path(ontology_name, algorithm, "embeddings.npy")
        with open(path, "rb") as f:
            embedding = numpy.load(f)
            return embedding[:no_class], embedding[no_class:]
    except Exception as e:
        raise FileException(f"Error loading embedding: {str(e)}")
