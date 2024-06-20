import os

from owl2vec_star.Label import pre_process_words
from models.ontology_model import getPath_ontology_directory  # type: ignore


def save_axioms(id, axioms):
    """Save axioms to a file

    Args:
        id (str): The id of the ontology
        axioms (list): The list of axioms to save
    Returns:
        list: The list of axioms saved to the file
    """
    path = os.path.join(getPath_ontology_directory(id), "axioms.txt")

    with open(path, "w", encoding="utf-8") as f:
        for axiom in axioms:
            f.write("%s\n" % axiom)

    return axioms


def save_classes(id, classes):
    """Save classes to a file

    Args:
        id (str): The id of the ontology
        classes (list): The list of classes to save
    Returns:
        list: The list of classes saved to the file
    """
    path = os.path.join(getPath_ontology_directory(id), "classes.txt")

    with open(path, "w", encoding="utf-8") as f:
        for cl in classes:
            f.write("%s\n" % cl)

    return classes


def save_individuals(id, individuals):
    """Save individuals to a file

    Args:
        id (str): The id of the ontology
        individuals (list): The list of individuals to save
    Returns:
        list: The list of individuals saved to the file
    """
    path = os.path.join(getPath_ontology_directory(id), "individuals.txt")

    with open(path, "w", encoding="utf-8") as f:
        for individual in individuals:
            f.write("%s\n" % individual)

    return individuals


def save_annotations(id, annotations, projection):
    """Save annotations to a file

    Args:
        id (str): The id of the ontology
        annotations (list): The list of annotations to save
        projection (Projection): The projection object
    Returns:
        list: The list of annotations saved to the file
    """
    lines = []

    # uri label
    path = os.path.join(getPath_ontology_directory(id), "uri_labels.txt")
    with open(path, "w", encoding="utf-8") as f:
        for e in projection.entityToPreferredLabels:
            for v in projection.entityToPreferredLabels[e]:
                f.write("%s %s\n" % (e, v))
    with open(path, "r", encoding="utf-8") as file:
        lines += file.readlines()

    # annotation
    path = os.path.join(getPath_ontology_directory(id), "annotations.txt")
    with open(path, "w", encoding="utf-8") as f:
        for a in annotations:
            f.write("%s\n" % " ".join(a))
    with open(path, "r", encoding="utf-8") as file:
        lines += file.readlines()

    return lines


def load_axioms(id):
    """Load axioms from a file

    Args:
        id (str): The id of the ontology
    Returns:
        list: The list of axioms loaded from the file
    """
    path = os.path.join(getPath_ontology_directory(id), "axioms.txt")

    return [line.strip() for line in open(path).readlines()]


def load_classes(id):
    """Load classes from a file

    Args:
        id (str): The id of the ontology
    Returns:
        list: The list of classes loaded from the file
    """
    path = os.path.join(getPath_ontology_directory(id), "classes.txt")

    return [line.strip() for line in open(path).readlines()]


def load_individuals(id):
    """Load individuals from a file

    Args:
        id (str): The id of the ontology
    Returns:
        list: The list of individuals loaded from the file
    """
    path = os.path.join(getPath_ontology_directory(id), "individuals.txt")

    return [line.strip() for line in open(path).readlines()]


def load_annotations(id):
    """Load annotations from a file

    Args:
        id (str): The id of the ontology
    Returns:
        dict: The dictionary of uri labels and the list of annotations loaded from the file
    """
    uri_label, annotations = list(), list()

    path = os.path.join(getPath_ontology_directory(id), "uri_labels.txt")
    
    with open( path, "r", encoding="utf-8" ) as f:
        uri_label = f.readlines()
    
    path = os.path.join(getPath_ontology_directory(id), "annotations.txt")
    
    with open( path, "r", encoding="utf-8" ) as f:
        annotations = f.readlines()
            
    return uri_label, annotations


def save_infer(id, infers):
    """Save inferred ancestors to a file

    Args:
        id (str): The id of the ontology
        infers (list): The list of inferred ancestors to save
    Returns:
        list: The list of inferred ancestors saved to the file
    """
    path = os.path.join(getPath_ontology_directory(id), "inferred_ancestors.txt")

    with open(path, "w", encoding="utf-8") as f:
        for result in infers:
            f.write(result + "\n")

    return infers


def load_infer(id):
    """Load inferred ancestors from a file

    Args:
        id (str): The id of the ontology
    Returns:
        list: The list of inferred ancestors loaded from the file
    """
    path = os.path.join(getPath_ontology_directory(id), "inferred_ancestors.txt")

    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()
