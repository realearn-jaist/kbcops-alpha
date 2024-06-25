import networkx as nx
import pandas as pd
import os
import matplotlib.pyplot as plt
from models.graph_model import load_graph
from utils.file_handler import replace_or_create_folder
from models.evaluator_model import read_garbage_metrics_pd
from models.ontology_model import get_path_ontology, get_path_ontology_directory
from models.extract_model import load_classes, load_individuals
from owlready2 import *

## Refactor code from https://github.com/realearn-jaist/kbc-ops/blob/main/app.py  ###########
#############################################################################################


def extract_garbage_value(onto_data):
    """Extracts the individual, true, and predicted values from the garbage metrics file

    Args:
        onto_data (pd.DataFrame): The garbage metrics file
    Returns:
        individual_list (list): The list of individuals
    """
    # Extract columns into lists
    class_individual_list = onto_data["Individual"].tolist()
    truth_list = onto_data["True"].tolist()
    predict_list = onto_data["Predicted"].tolist()

    return class_individual_list, truth_list, predict_list


def find_parents_with_relations(cls, splitter, relation_list=None):
    """Find the parents of a class and its relations

    Args:
        cls (owlready2.entity.ThingClass): The class to find the parents of
        relation_list (list, optional): The list of relations to append to. Defaults to None.
    
    Returns:
        list: List of relations in the form of [child_class_name, "subclassOf", parent_class_name]
    """
    if relation_list is None:
        relation_list = []

    # split = "obo."  # Assuming this is required for formatting class names

    try:
        parents = cls.is_a
        for parent in parents:
            if parent != owl.Thing:
                relation_list.append([
                    str(cls).split(splitter)[-1].split(")")[0],
                    "subclassOf",
                    str(parent).split(splitter)[-1].split(")")[0],
                ])
                # Recursively find parents' relations
                relation_list.extend(find_parents_with_relations(parent, splitter))
            else:
                relation_list.append([
                    str(cls).split(splitter)[-1].split(")")[0],
                    "subclassOf",
                    str(parent).split(splitter)[-1].split(")")[0],
                ])
    except Exception as e:
        pass

    return relation_list


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
    """Create a graph for each individual in the individual list

    Args:
        onto_type (str): The type of ontology "ABox" or "TBox"
        onto_file (owlready2.namespace.Ontology): The ontology file
        entity_prefix (str): The prefix of the entity
        individual_list (list): The list of individuals
        truth_list (list): The list of ground truth values
        predict_list (list): The list of predicted values
        fig_directory (str): The directory to save the graph figures
    Returns:
        None
    """
    replace_or_create_folder(fig_directory)
    for i, v in enumerate(class_individual_list):
        entity_uri = entity_prefix + v
        entity = onto_file.search(iri=entity_uri)[0]
        subs = entity.INDIRECT_is_a

        relations = list()

        if onto_type == "TBox":
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

        relations = [relation for relation in relations if relation[0] != relation[2]]

        G = nx.DiGraph()
        for rel in relations:
            source, relation, target = rel
            G.add_edge(source, target, label=relation)
            G.add_nodes_from([source, target])

        G.add_edge(class_individual_list[i], predict_list[i], label='predict')

        node_colors = [
            (
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
            for node in G.nodes()
        ]

        # Draw the graph
        plt.figure(figsize=(20, len(relations) * 2))
        pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=1500,
            node_color=node_colors,
            font_size=12,
            font_weight="bold",
        )
        for edge, label in nx.get_edge_attributes(G, "label").items():
            x = (pos[edge[0]][0] + pos[edge[1]][0]) / 2
            y = (pos[edge[0]][1] + pos[edge[1]][1]) / 2
            plt.text(
                x, y, label, horizontalalignment="center", verticalalignment="center"
            )

        plt.savefig(f"{fig_directory}\graph_{i}.png", format="PNG")


def create_graph(ontology_name, algorithm):
    # ontology_name, algorithm
    """Create a graph for each class and individual in the ontology
    Args:
        onto (str): The name of the ontology
        algo (str): The name of the algorithm
    Returns:
        list: The list of graph fig
    """
    # load individuals for checking whether it Tbox or not, and finding its prefix.
    fig_directory = os.path.join(
        get_path_ontology_directory(ontology_name), algorithm, "graph_fig"
    )  # where graph fig is save
    replace_or_create_folder(fig_directory)

    individuals = load_individuals(ontology_name)
    individuals_count = len(individuals)

    classes = [line.strip() for line in load_classes(ontology_name)]

    # check onto type
    # consider as a ABox iff individuals_count is excess 10 percent of classes amount
    onto_type = "ABox" if individuals_count > int(0.1 * len(classes)) else "TBox"

    # load ontology
    onto_file_path = get_path_ontology(ontology_name)
    onto = get_ontology(onto_file_path).load()

    # get prefix and its splitter
    tmp_class_ind = individuals[0]

    entity_prefix = get_prefix(tmp_class_ind)

    entity = onto.search(iri=tmp_class_ind)[0]
    entity_split = str(entity).split('.')[0] + '.'


    garbage_file = read_garbage_metrics_pd(ontology_name, algorithm)

    class_individual_list, truth_list, predict_list = extract_garbage_value(garbage_file)
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

    return load_graph(ontology_name, algorithm)


#############################################################################################
#############################################################################################
