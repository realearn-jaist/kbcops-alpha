import networkx as nx
import pandas as pd
import os
import matplotlib.pyplot as plt
import pydot
from models.graph_model import load_graph
from utils.directory_utils import get_path, replace_or_create_folder
from models.evaluator_model import read_garbage_metrics_pd
from models.extract_model import load_multi_input_files, coverage_class
from owlready2 import *

from utils.exceptions import (
    FileException,
    ModelException,
    EvaluationException,
    ExtractionException,
    GraphException,
)

## Refactor code from https://github.com/realearn-jaist/kbc-ops/blob/main/app.py  ###########
#############################################################################################


def extract_garbage_value(onto_data):
    """Extracts the individual, true, and predicted values from the garbage metrics file

    Args:
        onto_data (pd.DataFrame): The garbage metrics file
    Returns:
        individual_list (list): The list of individuals
    """
    try:
        # Extract columns into lists
        class_individual_list = onto_data["Individual"].tolist()
        truth_list = onto_data["True"].tolist()
        predict_list = onto_data["Predicted"].tolist()

        return class_individual_list, truth_list, predict_list

    except KeyError as e:
        raise GraphException(f"KeyError: {str(e)} occurred while extracting data")
    except Exception as e:
        raise GraphException(f"Error extracting garbage metrics: {str(e)}")


def find_parents_with_relations(cls, splitter, relation_list=None):
    """Find the parents of a class and its relations

    Args:
        cls (owlready2.entity.ThingClass): The class to find the parents of
        splitter (str): The string used to split class names
        relation_list (list, optional): The list of relations to append to. Defaults to None.

    Returns:
        list: list of relations
    """
    if relation_list is None:
        relation_list = []

    try:
        # Splitter is assumed to be defined elsewhere in your code

        parents = cls.is_a
        for parent in parents:
            if parent != owl.Thing:
                relation_list.append(
                    [
                        str(cls).split(splitter)[-1].split(")")[0],
                        "subclassOf",
                        str(parent).split(splitter)[-1].split(")")[0],
                    ]
                )
                # Recursively find parents' relations
                relation_list.extend(find_parents_with_relations(parent, splitter))
            else:
                relation_list.append(
                    [
                        str(cls).split(splitter)[-1].split(")")[0],
                        "subclassOf",
                        str(parent).split(splitter)[-1].split(")")[0],
                    ]
                )

        return relation_list

    except Exception as e:
        raise GraphException(f"Error in finding parents with relations: {str(e)}")


def get_prefix(value):
    """Get the prefix of the value because in ontology the class and individual id are separated by # or /

    Args:
        value (str): The value to get the prefix of
    Returns:
        prefix (str): The prefix of the value
    """
    delimiter = "#" if "#" in value else "/"
    prefix = value.rsplit(delimiter, 1)[0] + delimiter
    return prefix


def graph_maker(
    onto_type,
    onto_file,
    entity_prefix,
    entity_split,
    class_individual_list,
    truth_list,
    predict_list,
    fig_directory,
):
    """Create a DOT file for each individual.

    Args:
        onto_type (str): The type of ontology "abox" or "tbox".
        onto_file (owlready2.namespace.Ontology): The ontology file.
        entity_prefix (str): The prefix of the entity.
        entity_split (str): The splitter for entity names.
        class_individual_list (list): The list of individuals.
        truth_list (list): The list of ground truth values.
        predict_list (list): The list of predicted values.
        fig_directory (str): The directory to save the DOT files.

    Returns:
        None
    """
    try:
        for i, v in enumerate(class_individual_list):
            entity_uri = entity_prefix + v
            entity = onto_file.search(iri=entity_uri)[0]
            subs = entity.INDIRECT_is_a

            relations = []

            if onto_type == "tbox":
                relations = find_parents_with_relations(entity, entity_split)
            else:
                subs = sorted(list(subs), key=lambda sub: len(list(sub.INDIRECT_is_a)))
                subs = [
                    str(sub).split(".")[-1] if str(sub) != "owl.Thing" else str(sub)
                    for sub in subs
                ]
                for j in range(len(subs) - 1):
                    relations.append([subs[j + 1], "subclassOf", subs[j]])
                relations.append([str(entity).split(".")[-1], "isA", subs[-1]])

            relations = [
                relation for relation in relations if relation[0] != relation[2]
            ]

            dot_string = "digraph G {\n"
            
            nodes = set()
            for rel in relations:
                source, relation, target = rel
                dot_string += f'  "{source}" -> "{target}" [label="{relation}"];\n'
                nodes.add(source)
                nodes.add(target)
                

            dot_string += f'  "{v}" -> "{predict_list[i]}" [label="predict"];\n'
            
            # Set node colors
            for node in nodes:
                fill_color = (
                    "gray"
                    if node != truth_list[i]
                    and node != class_individual_list[i]
                    and node != predict_list[i]
                    else (
                        "#94F19C"
                        if node == truth_list[i]
                        else "#FC865A" if node == predict_list[i] else "#9DF1F0"
                    )
                )
                if fill_color:
                    dot_string += f'  "{node}" [style=filled,fillcolor="{fill_color}"];\n'                    
        
            dot_string += "}\n"
            
            # Save DOT string to file
            dot_file_path = os.path.join(fig_directory, f"graph_{i}.dot")
            with open(dot_file_path, 'w') as f:
                f.write(dot_string)
                
    except Exception as e:

        raise GraphException(f"Error creating graph: {str(e)}")



def create_graph(ontology_name, algorithm, classifier):
    # ontology_name, algorithm
    """Create a graph for each class and individual in the ontology
    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
        classifier (str): The name of the classifier
    Returns:
        list: The list of graph fig
    """
    try:
        # load individuals for checking whether it Tbox or not, and finding its prefix.
        fig_directory = get_path(ontology_name, algorithm, classifier, "graph_fig")
        replace_or_create_folder(fig_directory)

        # check onto type
        # consider as a ABox iff individuals_count is excess 10 percent of classes amount
        coverage_class_percentage = coverage_class(ontology_name)
        onto_type = "abox" if coverage_class_percentage > 10 else "tbox"

        # Load ontology file
        world = World()
        onto_file_path = get_path(ontology_name, ontology_name + ".owl")
        onto = world.get_ontology(onto_file_path).load()
        sync_reasoner(onto)
        input_files = ["individuals", "classes"]
        files = load_multi_input_files(ontology_name, input_files)

        # get prefix and its splitter
        if onto_type == "ABox":
            individuals = files["individuals"]
            tmp_class_ind = individuals[0]
        else:
            classes = files["classes"]
            tmp_class_ind = classes[0]

        entity_prefix = get_prefix(tmp_class_ind)
        entity = onto.search(iri=tmp_class_ind)[0]
        entity_split = ".".join(str(entity).rsplit(".")[:-1]) + "."

        # Read garbage metrics file
        garbage_file = read_garbage_metrics_pd(ontology_name, algorithm, classifier)
        class_individual_list, truth_list, predict_list = extract_garbage_value(
            garbage_file
        )

        # Create graphs for each class and individual
        graph_maker(
            onto_type,
            onto,
            entity_prefix,
            entity_split,
            class_individual_list,
            truth_list,
            predict_list,
            fig_directory,
        )

        # Load and return generated graph figures
        return load_graph(ontology_name, algorithm, classifier)

    except FileNotFoundError as e:
        raise FileException(f"File not found: {str(e)}", 404)
    except ValueError as e:
        raise GraphException(f"Input error: {str(e)}")
    except Exception as e:
        raise GraphException(f"Unexpected error: {str(e)}")


#############################################################################################
#############################################################################################
