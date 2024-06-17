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

nltk.download("punkt")

from models.extract_model import load_annotations, load_axioms, load_classes, load_individuals
from utils.file_handler import replace_or_create_folder
from models.embed_model import isModelExist, save_model
from models.ontology_model import getPath_ontology, getPath_ontology_directory
from owl2vec_star.RDF2Vec_Embed import get_rdf2vec_walks, get_rdf2vec_embed
from owl2vec_star.Label import pre_process_words, URI_parse
from owl2vec_star.Onto_Projection import Reasoner, OntologyProjection


def opa2vec_or_onto2vec(
    ontology_name, config_file, algorithm
):
    # get config
    config = configparser.ConfigParser()
    config.read(config_file)

    # retrieve file
    axioms = load_axioms(ontology_name)
    classes = load_classes(ontology_name)
    individuals = load_individuals(ontology_name)
    annotations = load_annotations(ontology_name)

    if algorithm == "opa2vec":
        lines = ( axioms + annotations )
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
    
    # path = os.path.join(getPath_ontology_directory(ontology_name), algorithm, "model")
    # w2v.save(path)
    # gensim.models.word2vec.Word2Vec.load(path)
    
    save_model(ontology_name, algorithm, w2v)
    return f"{algorithm} embedded success!!"


def owl2vec_star(ontology_name, config_file, algorithm):
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # retrieve file
    axioms = load_axioms(ontology_name)
    classes = load_classes(ontology_name)
    individuals = load_individuals(ontology_name)
    entities = classes.union(individuals)
    annotations_load = load_annotations(ontology_name)

    # preprocess annotations file
    uri_label, annotations = dict(), list()
    for line in annotations_load:
        tmp = line.strip().split()
        if tmp[1] == "http://www.w3.org/2000/01/rdf-schema#label":
            uri_label[tmp[0]] = pre_process_words(tmp[2:])
        else:
            annotations.append([tmp[0]] + tmp[2:])
            
    # structural doc
    walk_sentences, axiom_sentences, URI_Doc = list(), list(), list()
    if (
        "URI_Doc" in config["DOCUMENT_OWL2VECSTAR"]
        and config["DOCUMENT_OWL2VECSTAR"]["URI_Doc"] == "yes"
    ):
        print("\nGenerate URI document ...")
        walks_ = get_rdf2vec_walks(
            onto_file=getPath_ontology(ontology_name),
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

    save_model(ontology_name, algorithm, model_)
    return f"{algorithm} embedded success!!"


def rdf2vec(ontology_name, config_file, algorithm):
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # retrieve file
    axioms = load_axioms(ontology_name)
    classes = load_classes(ontology_name)
    individuals = load_individuals(ontology_name)
    entities = classes.union(individuals)
    annotations_load = load_annotations(ontology_name)
    candidate_num = len(classes)

    _temp, model_rdf2vec = get_rdf2vec_embed(
        onto_file=getPath_ontology(ontology_name),
        walker_type=config["MODEL_RDF2VEC"]["walker"],
        walk_depth=int(config["MODEL_RDF2VEC"]["walk_depth"]),
        embed_size=int(config["BASIC"]["embed_size"]),
        classes=entities,
    )
    
    save_model(ontology_name, algorithm, model_rdf2vec)
    return f"{algorithm} embedded success!!"


def embed_func(ontology_name, algorithm):
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
