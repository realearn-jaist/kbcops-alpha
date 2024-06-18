import networkx as nx
import pandas as pd
import os
import matplotlib.pyplot as plt
import models.extract_model as em
from owlready2 import *


def load_file(id):
    # load garbage information
    grabage_file_path = f"backend\storage\{id}\{id}_garbage.csv"
    grabage_file = pd.read_csv(os.path.abspath(grabage_file_path))

    # load onto file
    onto_file_path = f"backend\storage\{id}\{id}.owl"
    onto_file = get_ontology(os.path.abspath(onto_file_path)).load()

    return onto_file, grabage_file


def extract_grabage_value(onto_data):
    # turn csv into list
    individual_list = [x for x in list(onto_data["Individual"].tolist())]
    truth_list = [x for x in list(onto_data["True"].tolist())]
    predict_list = [x for x in list(onto_data["Predicted"].tolist())]

    return individual_list, truth_list, predict_list


def find_parents_with_relations(cls, relation_list):
    # find its relations
    try:
        parents = cls.is_a
        for parent in parents:
            if parent != owl.Thing:
                relation_list.append(
                    [
                        str(cls).split("obo.")[-1].split(")")[0],
                        "subclassOf",
                        str(parent).split("obo.")[-1].split(")")[0],
                    ]
                )
                find_parents_with_relations(parent, relation_list)
            else:
                relation_list.append(
                    [
                        str(cls).split("obo.")[-1].split(")")[0],
                        "subclassOf",
                        str(parent).split("obo.")[-1].split(")")[0],
                    ]
                )
    except Exception as e:
        pass


def get_prefix(value):
    delimiter = "#" if "#" in value else "/"
    prefix = value.rsplit(delimiter, 1)[0] + delimiter
    return prefix


def graph_maker(onto_type, entity_prefix, individual_list, truth_list, predict_list):
    # hard code first for foodon
    entity_prefix = "http://purl.obolibrary.org/obo/"

    for i, v in enumerate(individual_list):

        entity_uri = entity_prefix + v
        entity = ONTO.search(iri=entity_uri)[0]
        subs = entity.INDIRECT_is_a

        relations = list()

        if onto_type == "TBox":
            find_parents_with_relations(entity, relations)
        else:
            subs = sorted(list(subs), key=lambda sub: len(list(sub.INDIRECT_is_a)))
            subs = [
                str(sub).split(".")[-1] if str(sub) != "owl.Thing" else str(sub)
                for sub in subs
            ]
            for i in range(len(subs) - 1):
                relations.append([subs[i + 1], "subclassOf", subs[i]])
            relations.append([str(entity).split(".")[-1], "isA", subs[-1]])

        relations = [relation for relation in relations if relation[0] != relation[2]]

        G = nx.DiGraph()
        for rel in relations:
            source, relation, target = rel
            G.add_edge(source, target, label="subclassOf")
            G.add_nodes_from([source, target])

        node_colors = [
            (
                "gray"
                if node not in truth_list[i]
                and node not in individual_list[i]
                and node not in predict_list[i]
                else (
                    "#94F19C"
                    if node in truth_list[i]
                    else "#FC865A" if node in predict_list[i] else "#9DF1F0"
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

        plt.savefig(
            f"backend\storage\{id}\{id}\graph_fig\graph_{i+1}.png", format="PNG"
        )


def create_graph(id):
    # load omdividuals for checking whether it Tbox or not. And find its prefix
    individuals = em.load_individuals(id)

    individuals_count = len(em.load_individuals(id))
    onto_type = "TBox" if individuals_count > 0 else "ABox"

    entity_prefix = get_prefix(individuals.pop())

    onto_file, grabage_file = load_file(id)
    individual_list, truth_list, predict_list = extract_grabage_value(grabage_file)
    graph_maker(onto_type, entity_prefix, individual_list, truth_list, predict_list)

    return f"create graphs success!!"
