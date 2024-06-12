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

from models.ontology_model import getPath_ontology
from owl2vec_star.RDF2Vec_Embed import get_rdf2vec_walks, get_rdf2vec_embed
from owl2vec_star.Label import pre_process_words, URI_parse
from owl2vec_star.Onto_Projection import Reasoner, OntologyProjection


def opa2vec_or_onto2vec(
    ontology_file, ontology_name, embedding_dir, config_file, algorithm
):
    projection = OntologyProjection(
        ontology_file,
        reasoner=Reasoner.STRUCTURAL,
        only_taxonomy=False,
        bidirectional_taxonomy=True,
        include_literals=True,
        avoid_properties=set(),
        additional_preferred_labels_annotations=set(),
        additional_synonyms_annotations=set(),
        memory_reasoner="13351",
    )

    if not os.path.exists(f"backend/storage/{ontology_name}/{algorithm}"):
        print(f"backend/storage/{ontology_name}/{algorithm}")
        os.makedirs(f"backend/storage/{ontology_name}/{algorithm}")

    axiom_file = os.path.join(f"backend/storage/{ontology_name}/", "axioms.txt")
    projection.extractEntityURIs()
    classes = projection.getClassURIs()
    individuals = projection.getIndividualURIs()
    entities = classes.union(individuals)
    projection.indexAnnotations()
    uri_label, annotations = dict(), list()
    for e in entities:
        if (
            e in projection.entityToPreferredLabels
            and len(projection.entityToPreferredLabels[e]) > 0
        ):
            label = list(projection.entityToPreferredLabels[e])[0]
            uri_label[e] = pre_process_words(words=label.split())
    for e in entities:
        if e in projection.entityToAllLexicalLabels:
            for v in projection.entityToAllLexicalLabels[e]:
                if (v is not None) and (
                    not (
                        e in projection.entityToPreferredLabels
                        and v in projection.entityToPreferredLabels[e]
                    )
                ):
                    annotation = [e] + v.split()
                    annotations.append(annotation)

    annotation_file = os.path.join(
        f"backend/storage/{ontology_name}/", "annotations.txt"
    )

    if algorithm.lower() == "opa2vec":
        lines = (
            open(axiom_file, encoding="utf-8").readlines()
            + open(annotation_file, encoding="utf-8").readlines()
        )
    else:  # embedding_type.lower() == 'onto2vec'
        lines = open(axiom_file, encoding="utf-8").readlines()

    sentences = [
        [item.strip().lower() for item in line.strip().split()] for line in lines
    ]
    config = configparser.ConfigParser()
    config.read(config_file)

    if (
        config["MODEL_OPA2VEC_ONTO2VEC"]["pretrained"] == "none"
        or config["MODEL_OPA2VEC_ONTO2VEC"]["pretrained"] == ""
    ):
        sg_v = 1 if config["MODEL_OPA2VEC_ONTO2VEC"]["model"] == "sg" else 0
        w2v = gensim.models.Word2Vec(
            sentences,
            sg=sg_v,
            min_count=int(config["MODEL_OPA2VEC_ONTO2VEC"]["mincount"]),
            vector_size=int(config["BASIC"]["embed_size"]),
            window=int(config["MODEL_OPA2VEC_ONTO2VEC"]["windsize"]),
            workers=multiprocessing.cpu_count(),
        )
    else:
        w2v = gensim.models.Word2Vec.load(
            config["MODEL_OPA2VEC_ONTO2VEC"]["pretrained"]
        )
        w2v.min_count = int(config["MODEL_OPA2VEC_ONTO2VEC"]["mincount"])
        w2v.build_vocab(sentences, update=True)
        w2v.train(sentences, total_examples=w2v.corpus_count, epochs=100)

    classes_e = [
        (
            w2v.wv.get_vector(c.lower())
            if c.lower() in w2v.wv.index_to_key
            else np.zeros(w2v.vector_size)
        )
        for c in classes
    ]
    classes_e = np.array(classes_e)
    individuals_e = [
        (
            w2v.wv.get_vector(i.lower())
            if i.lower() in w2v.wv.index_to_key
            else np.zeros(w2v.vector_size)
        )
        for i in individuals
    ]
    individuals_e = np.array(individuals_e)
    w2v.save(embedding_dir)
    return f"{algorithm} embedded success!!"


def owl2vec_star(ontology_file, ontology_name, embedding_dir, config_file, algorithm):
    config = configparser.ConfigParser()
    config.read(config_file)

    if not os.path.exists(f"backend/storage/{ontology_name}/{algorithm}"):
        print(f"backend/storage/{ontology_name}/{algorithm}")
        os.makedirs(f"backend/storage/{ontology_name}/{algorithm}")

    start_time = time.time()
    if (
        (
            "ontology_projection" in config["DOCUMENT_OWL2VECSTAR"]
            and config["DOCUMENT_OWL2VECSTAR"]["ontology_projection"] == "yes"
        )
        or "pre_entity_file" not in config["DOCUMENT_OWL2VECSTAR"]
        or "pre_axiom_file" not in config["DOCUMENT_OWL2VECSTAR"]
        or "pre_annotation_file" not in config["DOCUMENT_OWL2VECSTAR"]
    ):
        print("\n Access the ontology ...")
        projection = OntologyProjection(
            ontology_file,
            reasoner=Reasoner.STRUCTURAL,
            only_taxonomy=False,
            bidirectional_taxonomy=True,
            include_literals=True,
            avoid_properties=set(),
            additional_preferred_labels_annotations=set(),
            additional_synonyms_annotations=set(),
            memory_reasoner="13351",
        )
    else:
        projection = None

    if (
        "ontology_projection" in config["DOCUMENT_OWL2VECSTAR"]
        and config["DOCUMENT_OWL2VECSTAR"]["ontology_projection"] == "yes"
    ):
        print("\nCalculate the ontology projection ...")
        projection.extractProjection()
        onto_projection_file = os.path.join(
            f"backend/storage/{ontology_name}/", "projection.ttl"
        )
        print("Save the projection graph to %s" % onto_projection_file)
        projection.saveProjectionGraph(onto_projection_file)
        ontology_file = onto_projection_file
    else:
        ontology_file = config["BASIC"]["ontology_file"]

    if "pre_entity_file" in config["DOCUMENT_OWL2VECSTAR"]:
        entities = [
            line.strip()
            for line in open(
                config["DOCUMENT_OWL2VECSTAR"]["pre_entity_file"]
            ).readlines()
        ]
    else:
        print("\nExtract classes and individuals ...")
        projection.extractEntityURIs()
        classes = projection.getClassURIs()
        individuals = projection.getIndividualURIs()
        entities = classes.union(individuals)

    if "pre_axiom_file" not in config["DOCUMENT_OWL2VECSTAR"]:
        print("\nExtract axioms ...")
        projection.createManchesterSyntaxAxioms()
    uri_label, annotations = dict(), list()

    if "pre_annotation_file" in config["DOCUMENT_OWL2VECSTAR"]:
        with open(config["DOCUMENT_OWL2VECSTAR"]["pre_annotation_file"]) as f:
            for line in f.readlines():
                tmp = line.strip().split()
                if tmp[1] == "http://www.w3.org/2000/01/rdf-schema#label":
                    uri_label[tmp[0]] = pre_process_words(tmp[2:])
                else:
                    annotations.append([tmp[0]] + tmp[2:])
    else:
        print("\nExtract annotations ...")
        projection.indexAnnotations()
        for e in entities:
            if (
                e in projection.entityToPreferredLabels
                and len(projection.entityToPreferredLabels[e]) > 0
            ):
                label = list(projection.entityToPreferredLabels[e])[0]
                uri_label[e] = pre_process_words(words=label.split())
        for e in entities:
            if e in projection.entityToAllLexicalLabels:
                for v in projection.entityToAllLexicalLabels[e]:
                    if (v is not None) and (
                        not (
                            e in projection.entityToPreferredLabels
                            and v in projection.entityToPreferredLabels[e]
                        )
                    ):
                        annotation = [e] + v.split()
                        annotations.append(annotation)
    walk_sentences, axiom_sentences, URI_Doc = list(), list(), list()
    if (
        "URI_Doc" in config["DOCUMENT_OWL2VECSTAR"]
        and config["DOCUMENT_OWL2VECSTAR"]["URI_Doc"] == "yes"
    ):
        print("\nGenerate URI document ...")
        walks_ = get_rdf2vec_walks(
            onto_file=ontology_file,
            walker_type=config["DOCUMENT_OWL2VECSTAR"]["walker"],
            walk_depth=int(config["DOCUMENT_OWL2VECSTAR"]["walk_depth"]),
            classes=entities,
        )
        print("Extracted %d walks for %d seed entities" % (len(walks_), len(entities)))
        walk_sentences += [list(map(str, x)) for x in walks_]

        axiom_file = os.path.join(f"backend/storage/{ontology_name}/", "axioms.txt")
        if os.path.exists(axiom_file):
            for line in open(axiom_file).readlines():
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

    print("Time for document construction: %s seconds" % (time.time() - start_time))
    random.shuffle(all_doc)

    start_time = time.time()
    if "pre_train_model" not in config["MODEL_OWL2VECSTAR"] or not os.path.exists(
        config["MODEL_OWL2VECSTAR"]["pre_train_model"]
    ):
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
    else:
        print("\nFine-tune the pre-trained embedding model ...")
        model_ = gensim.models.Word2Vec.load(
            config["MODEL_OWL2VECSTAR"]["pre_train_model"]
        )
        if len(all_doc) > 0:
            model_.min_count = int(config["MODEL_OWL2VECSTAR"]["min_count"])
            model_.build_vocab(all_doc, update=True)
            model_.train(
                all_doc,
                total_examples=model_.corpus_count,
                epochs=int(config["MODEL_OWL2VECSTAR"]["epoch"]),
            )
    model_.save(embedding_dir)
    print(
        "Time for learning the embedding model: %s seconds" % (time.time() - start_time)
    )
    return f"{algorithm} embedded success!!"


def rdf2vec(ontology_file, ontology_name, embedding_dir, config_file, algorithm):
    if not os.path.exists(f"backend/storage/{ontology_name}/{algorithm}"):
        os.makedirs(f"backend/storage/{ontology_name}/{algorithm}")

    config = configparser.ConfigParser()
    config.read(config_file)
    projection = OntologyProjection(
        ontology_file,
        reasoner=Reasoner.STRUCTURAL,
        only_taxonomy=False,
        bidirectional_taxonomy=True,
        include_literals=True,
        avoid_properties=set(),
        additional_preferred_labels_annotations=set(),
        additional_synonyms_annotations=set(),
        memory_reasoner="13351",
    )

    projection.extractEntityURIs()
    classes = projection.getClassURIs()
    classes = list(classes)
    individuals = projection.getIndividualURIs()
    individuals = list(individuals)
    candidate_num = len(classes)

    all_e, model_rdf2vec = get_rdf2vec_embed(
        onto_file=ontology_file,
        walker_type=config["MODEL_RDF2VEC"]["walker"],
        walk_depth=int(config["MODEL_RDF2VEC"]["walk_depth"]),
        embed_size=int(config["BASIC"]["embed_size"]),
        classes=classes + individuals,
    )
    # classes_e, individuals_e = all_e[: len(classes)], all_e[len(classes) :]
    joblib.dump(model_rdf2vec, embedding_dir)
    return f"{algorithm} embedded success!!"


def embed_func(ontology_name, algorithm):
    ontology_file = getPath_ontology(ontology_name)
    embedding_dir = f"backend/storage/{ontology_name}/{algorithm}/model"
    config_file = "backend/controllers/default.cfg"

    algorithms = {
        "owl2vec-star": owl2vec_star,
        "rdf2vec": rdf2vec,
        "opa2vec": opa2vec_or_onto2vec,
        "onto2vec": opa2vec_or_onto2vec,
    }

    algorithm_key = algorithm.lower()
    if algorithm_key in algorithms:
        result = algorithms[algorithm_key](
            ontology_file=ontology_file,
            ontology_name=ontology_name,
            embedding_dir=embedding_dir,
            config_file=config_file,
            algorithm=algorithm_key,
        )
        return result
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
