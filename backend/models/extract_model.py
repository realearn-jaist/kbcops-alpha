import os
import owlready2

from models.ontology_model import get_path_ontology, get_path_ontology_directory  # type: ignore


def save_axioms(ontology_name, axioms):
    """Save axioms to a file

    Args:
        id (str): The id of the ontology
        axioms (list): The list of axioms to save
    Returns:
        list: The list of axioms saved to the file
    """
    path = os.path.join(get_path_ontology_directory(ontology_name), "axioms.txt")

    with open(path, "w", encoding="utf-8") as f:
        for axiom in axioms:
            f.write("%s\n" % axiom)

    return axioms


def save_classes(ontology_name, classes):
    """Save classes to a file

    Args:
        id (str): The id of the ontology
        classes (list): The list of classes to save
    Returns:
        list: The list of classes saved to the file
    """
    path = os.path.join(get_path_ontology_directory(ontology_name), "classes.txt")

    with open(path, "w", encoding="utf-8") as f:
        for cl in classes:
            f.write("%s\n" % cl)

    return classes


def save_individuals(ontology_name, individuals):
    """Save individuals to a file

    Args:
        id (str): The id of the ontology
        individuals (list): The list of individuals to save
    Returns:
        list: The list of individuals saved to the file
    """
    path = os.path.join(get_path_ontology_directory(ontology_name), "individuals.txt")

    with open(path, "w", encoding="utf-8") as f:
        for individual in individuals:
            f.write("%s\n" % individual)

    return individuals


def save_annotations(ontology_name, annotations, projection):
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
    path = os.path.join(get_path_ontology_directory(ontology_name), "uri_labels.txt")
    with open(path, "w", encoding="utf-8") as f:
        for e in projection.entityToPreferredLabels:
            for v in projection.entityToPreferredLabels[e]:
                f.write("%s %s\n" % (e, v))
    with open(path, "r", encoding="utf-8") as file:
        lines += file.readlines()

    # annotation
    path = os.path.join(get_path_ontology_directory(ontology_name), "annotations.txt")
    with open(path, "w", encoding="utf-8") as f:
        for a in annotations:
            f.write("%s\n" % " ".join(a))
    with open(path, "r", encoding="utf-8") as file:
        lines += file.readlines()

    return lines

def load_multi_input_files(ontology_name, files_list):
    """Load multiple input files

    Args:
        ontology_name (str): The name of the ontology
        input_file (str): The name of the input file
    Returns:
        list: The list of axioms loaded from the file
    """
    files_dict = dict()
    for value in files_list:
        tmp = load_input_file(ontology_name, value + '.txt')
        files_dict[value] = tmp
    return files_dict
     

def load_input_file(ontology_name, input_file):
    """Load single the input file

    Args:
        ontology_name (str): The name of the ontology
        input_file (str): The name of the input file
    Returns:
        list: The list of axioms loaded from the file
    """
    path = os.path.join(get_path_ontology_directory(ontology_name), input_file)

    return [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]
    

def load_axioms(ontology_name):
    """Load axioms from a file

    Args:
        id (str): The id of the ontology
    Returns:
        list: The list of axioms loaded from the file
    """
    path = os.path.join(get_path_ontology_directory(ontology_name), "axioms.txt")

    return [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]


def load_classes(ontology_name):
    """Load classes from a file

    Args:
        id (str): The id of the ontology
    Returns:
        list: The list of classes loaded from the file
    """
    path = os.path.join(get_path_ontology_directory(ontology_name), "classes.txt")

    return [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]


def load_individuals(ontology_name):
    """Load individuals from a file

    Args:
        id (str): The id of the ontology
    Returns:
        list: The list of individuals loaded from the file
    """
    path = os.path.join(get_path_ontology_directory(ontology_name), "individuals.txt")

    return [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]


def load_annotations(ontology_name):
    """Load annotations from a file

    Args:
        id (str): The id of the ontology
    Returns:
        dict: The dictionary of uri labels and the list of annotations loaded from the file
    """
    uri_label, annotations = list(), list()

    path = os.path.join(get_path_ontology_directory(ontology_name), "uri_labels.txt")
    
    with open( path, "r", encoding="utf-8" ) as f:
        uri_label = [line.strip() for line in f.readlines()]
    
    path = os.path.join(get_path_ontology_directory(ontology_name), "annotations.txt")
    
    with open( path, "r", encoding="utf-8" ) as f:
        annotations = [line.strip() for line in f.readlines()]
            
    return uri_label, annotations


def save_infer(ontology_name, infers):
    """Save inferred ancestors to a file

    Args:
        id (str): The id of the ontology
        infers (list): The list of inferred ancestors to save
    Returns:
        list: The list of inferred ancestors saved to the file
    """
    path = os.path.join(get_path_ontology_directory(ontology_name), "inferred_ancestors.txt")

    with open(path, "w", encoding="utf-8") as f:
        for result in infers:
            f.write(result + "\n")

    return infers


def load_infer(ontology_name):
    """Load inferred ancestors from a file

    Args:
        id (str): The id of the ontology
    Returns:
        list: The list of inferred ancestors loaded from the file
    """
    path = os.path.join(get_path_ontology_directory(ontology_name), "inferred_ancestors.txt")

    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()
    
def coverage_class(ontology_name):
    
    path = get_path_ontology(ontology_name)
    onto = owlready2.get_ontology(path).load()
    coverage_class = set()

    # Iterate through all individuals and add their classes to the set
    for individual in onto.individuals():
        for cls in individual.is_a:
            if isinstance(cls, owlready2.ThingClass):
                coverage_class.add(cls)

    # Count the unique classes
    unique_class_count = len(coverage_class)
    total_classes = len(list(onto.classes()))

    if unique_class_count > 0:
        coverage_percentage = (unique_class_count / total_classes) * 100
    else:
        coverage_percentage = 0
    return coverage_percentage