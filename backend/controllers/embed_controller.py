from flask import jsonify, render_template, request
import joblib
import numpy as np
import os
import time
import argparse
import random
import multiprocessing
import gensim
import configparser
import nltk
import numpy

nltk.download("punkt")

from models.extract_model import (
    load_annotations,
    load_axioms,
    load_classes,
    load_individuals,
)
from models.embed_model import isModelExist, save_embedding, save_model
from models.ontology_model import get_path_ontology
from owl2vec_star.RDF2Vec_Embed import get_rdf2vec_walks, get_rdf2vec_embed
from owl2vec_star.Label import pre_process_words, URI_parse


def opa2vec_or_onto2vec(ontology_name, config_file, algorithm):
    """Embedding function for OPA2Vec and Onto2Vec

    Args:
        ontology_name (str): The name of the ontology
        config_file (str): The path to the configuration file
        algorithm (str): The name of the algorithm
    Returns:
        str: The result of the embedding process
    """
    # get config
    config = configparser.ConfigParser()
    config.read(config_file)

    # retrieve file
    axioms = load_axioms(ontology_name)
    classes = load_classes(ontology_name)
    individuals = load_individuals(ontology_name)
    uri_label, annotations = load_annotations(ontology_name)

    if algorithm == "opa2vec":
        lines = axioms + annotations + uri_label
    else:  # embedding_type.lower() == 'onto2vec'
        lines = axioms

    sentences = [
        [item.strip().lower() for item in line.strip().split()] for line in lines
    ]

    # model word2vec
    sg_v = 1 if config["MODEL_OPA2VEC_ONTO2VEC"]["model"] == "sg" else 0
    w2v = gensim.models.Word2Vec(
        sentences,
        sg=sg_v,
        min_count=int(config["MODEL_OPA2VEC_ONTO2VEC"]["mincount"]),
        vector_size=int(config["BASIC"]["embed_size"]),
        window=int(config["MODEL_OPA2VEC_ONTO2VEC"]["windsize"]),
        workers=multiprocessing.cpu_count(),
    )

    embeddings = embed_opa_onto(w2v, classes + individuals)
    # classes_e, individuals_e = embed_opa_onto_temp(w2v, classes, individuals)

    save_model(ontology_name, algorithm, w2v)
    save_embedding(ontology_name, algorithm, embeddings)

    return f"{algorithm} embedded success!!"


def owl2vec_star(ontology_name, config_file, algorithm):
    """Embedding function for OWL2Vec-Star

    Args:
        ontology_name (str): The name of the ontology
        config_file (str): The path to the configuration file
        algorithm (str): The name of the algorithm
    Returns:
        str: The result of the embedding process
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    # retrieve file
    axioms = load_axioms(ontology_name)
    classes = load_classes(ontology_name)
    individuals = load_individuals(ontology_name)
    entities = classes + individuals
    uri_label_load, annotations_load = load_annotations(ontology_name)

    uri_label, annotations = dict(), list()

    for line in uri_label_load:
        tmp = line.strip().split()
        uri_label[tmp[0]] = pre_process_words(tmp[1:])
    for line in annotations_load:
        tmp = line.strip().split()
        annotations.append(tmp)

    # structural doc
    walk_sentences, axiom_sentences, URI_Doc = list(), list(), list()
    if (
        "URI_Doc" in config["DOCUMENT_OWL2VECSTAR"]
        and config["DOCUMENT_OWL2VECSTAR"]["URI_Doc"] == "yes"
    ):
        print("\nGenerate URI document ...")
        walks_ = get_rdf2vec_walks(
            onto_file=get_path_ontology(ontology_name),
            walker_type=config["DOCUMENT_OWL2VECSTAR"]["walker"],
            walk_depth=int(config["DOCUMENT_OWL2VECSTAR"]["walk_depth"]),
            classes=entities,
        )
        print("Extracted %d walks for %d seed entities" % (len(walks_), len(entities)))
        walk_sentences += [list(map(str, x)) for x in walks_]

        for line in axioms:
            axiom_sentence = [item for item in line.strip().split()]
            axiom_sentences.append(axiom_sentence)
        print("Extracted %d axiom sentences" % len(axiom_sentences))
        URI_Doc = walk_sentences + axiom_sentences

    def label_item(item):
        if item in uri_label:
            return uri_label[item]
        elif item.startswith("http://www.w3.org"):
            return [item.split("#")[1].lower()]
        elif item.startswith("http://"):
            return URI_parse(uri=item)
        else:
            return [item.lower()]

    # lit doc
    Lit_Doc = list()
    if (
        "Lit_Doc" in config["DOCUMENT_OWL2VECSTAR"]
        and config["DOCUMENT_OWL2VECSTAR"]["Lit_Doc"] == "yes"
    ):
        print("\nGenerate literal document ...")
        for annotation in annotations:
            processed_words = pre_process_words(annotation[1:])
            if len(processed_words) > 0:
                Lit_Doc.append(label_item(item=annotation[0]) + processed_words)
        print("Extracted %d annotation sentences" % len(Lit_Doc))

        for sentence in walk_sentences:
            lit_sentence = list()
            for item in sentence:
                lit_sentence += label_item(item=item)
            Lit_Doc.append(lit_sentence)

        for sentence in axiom_sentences:
            lit_sentence = list()
            for item in sentence:
                lit_sentence += label_item(item=item)
            Lit_Doc.append(lit_sentence)

    # mix doc
    Mix_Doc = list()
    if (
        "Mix_Doc" in config["DOCUMENT_OWL2VECSTAR"]
        and config["DOCUMENT_OWL2VECSTAR"]["Mix_Doc"] == "yes"
    ):
        print("\nGenerate mixture document ...")
        for sentence in walk_sentences + axiom_sentences:
            if config["DOCUMENT_OWL2VECSTAR"]["Mix_Type"] == "all":
                for index in range(len(sentence)):
                    mix_sentence = list()
                    for i, item in enumerate(sentence):
                        mix_sentence += [item] if i == index else label_item(item=item)
                    Mix_Doc.append(mix_sentence)
            elif config["DOCUMENT_OWL2VECSTAR"]["Mix_Type"] == "random":
                random_index = random.randint(0, len(sentence) - 1)
                mix_sentence = list()
                for i, item in enumerate(sentence):
                    mix_sentence += (
                        [item] if i == random_index else label_item(item=item)
                    )
                Mix_Doc.append(mix_sentence)

    print(
        "URI_Doc: %d, Lit_Doc: %d, Mix_Doc: %d"
        % (len(URI_Doc), len(Lit_Doc), len(Mix_Doc))
    )
    all_doc = URI_Doc + Lit_Doc + Mix_Doc

    random.shuffle(all_doc)

    # word2vec model
    print("\nTrain the embedding model ...")
    model_ = gensim.models.Word2Vec(
        all_doc,
        vector_size=int(config["BASIC"]["embed_size"]),
        window=int(config["MODEL_OWL2VECSTAR"]["window"]),
        workers=multiprocessing.cpu_count(),
        sg=1,
        epochs=int(config["MODEL_OWL2VECSTAR"]["iteration"]),
        negative=int(config["MODEL_OWL2VECSTAR"]["negative"]),
        min_count=int(config["MODEL_OWL2VECSTAR"]["min_count"]),
        seed=int(config["MODEL_OWL2VECSTAR"]["seed"]),
    )

    embeddings = embed_owl2vec(model_, classes + individuals)

    save_model(ontology_name, algorithm, model_)
    save_embedding(ontology_name, algorithm, embeddings)
    return f"{algorithm} embedded success!!"


def rdf2vec(ontology_name, config_file, algorithm):
    """Embedding function for RDF2Vec

    Args:
        ontology_name (str): The name of the ontology
        config_file (str): The path to the configuration file
        algorithm (str): The name of the algorithm
    Returns:
        str: The result of the embedding process
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    # retrieve file
    axioms = load_axioms(ontology_name)
    classes = load_classes(ontology_name)
    individuals = load_individuals(ontology_name)
    entities = classes + individuals
    uri_label, annotations = load_annotations(ontology_name)
    candidate_num = len(classes)

    embeddings, model_rdf2vec = get_rdf2vec_embed(
        onto_file=get_path_ontology(ontology_name),
        walker_type=config["MODEL_RDF2VEC"]["walker"],
        walk_depth=int(config["MODEL_RDF2VEC"]["walk_depth"]),
        embed_size=int(config["BASIC"]["embed_size"]),
        classes=entities,
    )

    save_model(ontology_name, algorithm, model_rdf2vec)
    save_embedding(ontology_name, algorithm, embeddings)
    return f"{algorithm} embedded success!!"


def embed_func(ontology_name, algorithm):
    """Embedding function for the given algorithm and ontology

    Args:
        ontology_name (str): The name of the ontology
        algorithm (str): The name of the algorithm
    Returns:
        str: The result of the embedding process
    """
    # check if system have ontology file and algorithm so that it can directly return the result
    if isModelExist(ontology_name, algorithm):
        result = f"{algorithm} model already exists for {ontology_name} ontology"
        return result

    config_file = "controllers/default.cfg"

    algorithms = {
        "owl2vec-star": owl2vec_star,
        "rdf2vec": rdf2vec,
        "opa2vec": opa2vec_or_onto2vec,
        "onto2vec": opa2vec_or_onto2vec,
    }

    if algorithm in algorithms:
        result = algorithms[algorithm](
            ontology_name=ontology_name,
            config_file=config_file,
            algorithm=algorithm,
        )
        return result
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def embed_owl2vec(model: gensim.models.Word2Vec, instances):
    """Embed instances using the given model

    Args:
        model (gensim.models.Word2Vec): The Word2Vec model
        instances (list): The list of instances to embed
    Returns:
        list: The list of embedded instances
    """
    feature_vectors = []
    for instance in instances:
        v_uri = (
            model.wv.get_vector(instance)
            if instance in model.wv.index_to_key
            else np.zeros(model.vector_size)
        )
        feature_vectors.append(v_uri)

    return feature_vectors


def embed_opa_onto(model: gensim.models.Word2Vec, instances):
    """Embed instances using the given model

    Args:
        model (gensim.models.Word2Vec): The Word2Vec model
        instances (list): The list of instances to embed
    Returns:
        list: The list of embedded instances
    """
    all_e = [
        (
            model.wv.get_vector(c.lower())
            if c.lower() in model.wv.index_to_key
            else np.zeros(model.vector_size)
        )
        for c in instances
    ]
    all_e = np.array(all_e)

    return all_e


# def embed_opa_onto_temp(w2v, classes, individuals):
#     classes_e = [
#         (
#             w2v.wv.get_vector(c.lower())
#             if c.lower() in w2v.wv.index_to_key
#             else np.zeros(w2v.vector_size)
#         )
#         for c in classes
#     ]
#     classes_e = np.array(classes_e)

#     individuals_e = [
#         (
#             w2v.wv.get_vector(i.lower())
#             if i.lower() in w2v.wv.index_to_key
#             else np.zeros(w2v.vector_size)
#         )
#         for i in individuals
#     ]
#     individuals_e = np.array(individuals_e)

#     all_e = np.concatenate((classes_e, individuals_e))

#     return classes_e, individuals_e
