from flask import jsonify, render_template, request
from backend import app
import os
import time
import argparse
import random
import multiprocessing
import gensim
import configparser
import nltk

nltk.download('punkt')

from owl2vec_star.lib.RDF2Vec_Embed import get_rdf2vec_walks
from owl2vec_star.lib.Label import pre_process_words, URI_parse
from owl2vec_star.lib.Onto_Projection import Reasoner, OntologyProjection


def embed_predict_func(ontology_file, embedding_dir, config_file, algorithm):
    config = configparser.ConfigParser()
    config.read(config_file)
    print('config:', config.sections())
    print(config['DOCUMENT']['cache_dir'])
    if not os.path.exists(config['DOCUMENT']['cache_dir']):
        os.mkdir(config['DOCUMENT']['cache_dir'])
    #config['ALGORITHM']['selected_algorithm'] = algorithm
    start_time = time.time()
    if ('ontology_projection' in config['DOCUMENT'] and config['DOCUMENT']['ontology_projection'] == 'yes') or \
            'pre_entity_file' not in config['DOCUMENT'] or 'pre_axiom_file' not in config['DOCUMENT'] or \
            'pre_annotation_file' not in config['DOCUMENT']:
        print('\n Access the ontology ...')
        projection = OntologyProjection(ontology_file, reasoner=Reasoner.STRUCTURAL, only_taxonomy=False,
                                        bidirectional_taxonomy=True, include_literals=True, avoid_properties=set(),
                                        additional_preferred_labels_annotations=set(),
                                        additional_synonyms_annotations=set(),
                                        memory_reasoner='13351')
    else:
        projection = None

    if 'ontology_projection' in config['DOCUMENT'] and config['DOCUMENT']['ontology_projection'] == 'yes':
        print('\nCalculate the ontology projection ...')
        projection.extractProjection()
        onto_projection_file = os.path.join(config['DOCUMENT']['cache_dir'], 'projection.ttl')
        print('Save the projection graph to %s' % onto_projection_file)
        projection.saveProjectionGraph(onto_projection_file)
        ontology_file = onto_projection_file
    else:
        ontology_file = config['BASIC']['ontology_file']

    if 'pre_entity_file' in config['DOCUMENT']:
        entities = [line.strip() for line in open(config['DOCUMENT']['pre_entity_file']).readlines()]
    else:
        print('\nExtract classes and individuals ...')
        projection.extractEntityURIs()
        classes = projection.getClassURIs()
        individuals = projection.getIndividualURIs()
        entities = classes.union(individuals)
        with open(os.path.join(config['DOCUMENT']['cache_dir'], 'entities.txt'), 'w') as f:
            for e in entities:
                f.write('%s\n' % e)
                
    if 'pre_axiom_file' not in config['DOCUMENT']:
        print('\nExtract axioms ...')
        projection.createManchesterSyntaxAxioms()
        with open(os.path.join(config['DOCUMENT']['cache_dir'], 'axioms.txt'), 'w') as f:
            for ax in projection.axioms_manchester:
                f.write('%s\n' % ax)
    uri_label, annotations = dict(), list()

    if 'pre_annotation_file' in config['DOCUMENT']:
        with open(config['DOCUMENT']['pre_annotation_file']) as f:
            for line in f.readlines():
                tmp = line.strip().split()
                if tmp[1] == 'http://www.w3.org/2000/01/rdf-schema#label':
                    uri_label[tmp[0]] = pre_process_words(tmp[2:])
                else:
                    annotations.append([tmp[0]] + tmp[2:])
    else:
        print('\nExtract annotations ...')
        projection.indexAnnotations()
        for e in entities:
            if e in projection.entityToPreferredLabels and len(projection.entityToPreferredLabels[e]) > 0:
                label = list(projection.entityToPreferredLabels[e])[0]
                uri_label[e] = pre_process_words(words=label.split())
        for e in entities:
            if e in projection.entityToAllLexicalLabels:
                for v in projection.entityToAllLexicalLabels[e]:
                    if (v is not None) and \
                            (not (e in projection.entityToPreferredLabels and v in projection.entityToPreferredLabels[e])):
                        annotation = [e] + v.split()
                        annotations.append(annotation)

        with open(os.path.join(config['DOCUMENT']['cache_dir'], 'annotations.txt'), 'w', encoding='utf-8') as f:
            for e in projection.entityToPreferredLabels:
                for v in projection.entityToPreferredLabels[e]:
                    f.write('%s preferred_label %s\n' % (e, v))
            for a in annotations:
                f.write('%s\n' % ' '.join(a))

    walk_sentences, axiom_sentences, URI_Doc = list(), list(), list()
    if 'URI_Doc' in config['DOCUMENT'] and config['DOCUMENT']['URI_Doc'] == 'yes':
        print('\nGenerate URI document ...')
        walks_ = get_rdf2vec_walks(onto_file=ontology_file, walker_type=config['DOCUMENT']['walker'],
                                walk_depth=int(config['DOCUMENT']['walk_depth']), classes=entities)
        print('Extracted %d walks for %d seed entities' % (len(walks_), len(entities)))
        walk_sentences += [list(map(str, x)) for x in walks_]

        axiom_file = os.path.join(config['DOCUMENT']['cache_dir'], 'axioms.txt')
        if os.path.exists(axiom_file):
            for line in open(axiom_file).readlines():
                axiom_sentence = [item for item in line.strip().split()]
                axiom_sentences.append(axiom_sentence)
        print('Extracted %d axiom sentences' % len(axiom_sentences))
        URI_Doc = walk_sentences + axiom_sentences

    def label_item(item):
        if item in uri_label:
            return uri_label[item]
        elif item.startswith('http://www.w3.org'):
            return [item.split('#')[1].lower()]
        elif item.startswith('http://'):
            return URI_parse(uri=item)
        else:
            return [item.lower()]

    Lit_Doc = list()
    if 'Lit_Doc' in config['DOCUMENT'] and config['DOCUMENT']['Lit_Doc'] == 'yes':
        print('\nGenerate literal document ...')
        for annotation in annotations:
            processed_words = pre_process_words(annotation[1:])
            if len(processed_words) > 0:
                Lit_Doc.append(label_item(item=annotation[0]) + processed_words)
        print('Extracted %d annotation sentences' % len(Lit_Doc))

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
    if 'Mix_Doc' in config['DOCUMENT'] and config['DOCUMENT']['Mix_Doc'] == 'yes':
        print('\nGenerate mixture document ...')
        for sentence in walk_sentences + axiom_sentences:
            if config['DOCUMENT']['Mix_Type'] == 'all':
                for index in range(len(sentence)):
                    mix_sentence = list()
                    for i, item in enumerate(sentence):
                        mix_sentence += [item] if i == index else label_item(item=item)
                    Mix_Doc.append(mix_sentence)
            elif config['DOCUMENT']['Mix_Type'] == 'random':
                random_index = random.randint(0, len(sentence) - 1)
                mix_sentence = list()
                for i, item in enumerate(sentence):
                    mix_sentence += [item] if i == random_index else label_item(item=item)
                Mix_Doc.append(mix_sentence)

    print('URI_Doc: %d, Lit_Doc: %d, Mix_Doc: %d' % (len(URI_Doc), len(Lit_Doc), len(Mix_Doc)))
    all_doc = URI_Doc + Lit_Doc + Mix_Doc

    print('Time for document construction: %s seconds' % (time.time() - start_time))
    random.shuffle(all_doc)

    start_time = time.time()
    if 'pre_train_model' not in config['MODEL'] or not os.path.exists(config['MODEL']['pre_train_model']):
        print('\nTrain the embedding model ...')
        model_ = gensim.models.Word2Vec(all_doc, vector_size=int(config['MODEL']['embed_size']),
                                        window=int(config['MODEL']['window']),
                                        workers=multiprocessing.cpu_count(),
                                        sg=1, epochs=int(config['MODEL']['iteration']),
                                        negative=int(config['MODEL']['negative']),
                                        min_count=int(config['MODEL']['min_count']), seed=int(config['MODEL']['seed']))
    else:
        print('\nFine-tune the pre-trained embedding model ...')
        model_ = gensim.models.Word2Vec.load(config['MODEL']['pre_train_model'])
        if len(all_doc) > 0:
            model_.min_count = int(config['MODEL']['min_count'])
            model_.build_vocab(all_doc, update=True)
            model_.train(all_doc, total_examples=model_.corpus_count, epochs=int(config['MODEL']['epoch']))

    model_.save(embedding_dir)
    print('Time for learning the embedding model: %s seconds' % (time.time() - start_time))
    print('Model saved. Done!')
    return "Embed Model created successfully!"