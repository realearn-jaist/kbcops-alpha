import os
from owlready2 import *
from tqdm import tqdm
from collections import defaultdict

from models.extract_model import load_annotations, load_axioms, load_classes, load_individuals, save_annotations, save_axioms, save_classes, save_individuals, save_infer
from models.ontology_model import getPath_ontology_directory, list_ontology, save_ontology, getPath_ontology

from owl2vec_star.Onto_Projection import Reasoner, OntologyProjection # type: ignore
from owl2vec_star.Label import pre_process_words # type: ignore


def upload_ontology(file, id):
    if id.endswith('.owl'):
        id = id[:-4]

    filename = id + ".owl"
    
    path = save_ontology(file, id, filename)

    return id if path else None

def getAll_ontology():
    return list_ontology()

def get_onto_stat(id):
    axioms = load_axioms(id)
    classes = load_classes(id)
    individuals = load_individuals(id)
    annotations = load_annotations(id)
    
    return {
        "no_class": len(classes),
        "no_individual": len(individuals),
        "no_axiom": len(axioms),
        "no_annotation": len(annotations),
    }
        

def extract_data(id):
    onto_file = getPath_ontology(id)
    
    # extract axiom, entity, annotation
    projection = OntologyProjection(
        onto_file,
        reasoner=Reasoner.STRUCTURAL,
        only_taxonomy=False,
        bidirectional_taxonomy=True,
        include_literals=True,
        avoid_properties=set(),
        additional_preferred_labels_annotations=set(),
        additional_synonyms_annotations=set(),
        memory_reasoner="13351",
    )
    
    # axioms
    projection.createManchesterSyntaxAxioms()
    axioms = projection.axioms_manchester
    
    # entities (classes and individuals)
    projection.extractEntityURIs()
    classes = projection.getClassURIs()
    individuals = projection.getIndividualURIs()
    entities = classes.union(individuals)
    
    # annotations
    projection.indexAnnotations()
    uri_label, annotations = dict(), list()
    for e in tqdm(entities, desc="Processing Preferred Labels"):
        if (
            e in projection.entityToPreferredLabels
            and len(projection.entityToPreferredLabels[e]) > 0
        ):
            label = list(projection.entityToPreferredLabels[e])[0]
            uri_label[e] = pre_process_words(words=label.split())
    for e in tqdm(entities, desc="Processing Lexical Labels"):
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
                    
    axioms = save_axioms(id, axioms)
    classes = save_classes(id, classes)
    individuals = save_individuals(id, individuals)
    annotations = save_annotations(id, annotations, projection)
    
    # extract axiom, entity, annotation
    onto = get_ontology(getPath_ontology(id)).load()
    
    print("sync reasoner")
    sync_reasoner()
    
    tbox_results = tbox_infer(onto)
    abox_results = abox_infer(onto)
    
    save_infer(id, tbox_results + abox_results)
    
    return {
        "no_class": len(classes),
        "no_individual": len(individuals),
        "no_axiom": len(axioms),
        "no_annotation": len(annotations),
    }
    
def get_all_superclasses(cls, cache):
    if cls in cache:
        return cache[cls]
    
    superclasses = []
    for sc in cls.is_a:
        if sc != owl.Thing:
            superclasses.append(sc)
            superclasses.extend(get_all_superclasses(sc, cache))
    
    cache[cls] = superclasses
    return superclasses

def abox_infer(onto):
    superclass_cache = defaultdict(list)
    results = []
    for ind in tqdm(onto.individuals(), desc="Processing individuals"):
        ind_uri = ind.iri
        inferred_classes = get_all_superclasses(ind, superclass_cache)
        inferred_classes = inferred_classes[1:]
        inferred_classes_str = ",".join(
            cls.iri for cls in inferred_classes if hasattr(cls, "iri")
        )
        if inferred_classes_str and not inferred_classes_str.endswith(","):
            inferred_classes_str += ","
        inferred_classes_str += "owl:Thing"
        results.append(f"{ind_uri},{inferred_classes_str}")
    return results
            
def tbox_infer(onto):
    superclass_cache = defaultdict(list)
    results = []
    for cls in tqdm(onto.classes(), desc="Processing classes"):
        cls_uri = cls.iri
        inferred_classes = get_all_superclasses(cls, superclass_cache)
        inferred_classes = inferred_classes[1:]
        inferred_classes_str = ",".join(
            cls.iri for cls in inferred_classes if hasattr(cls, "iri")
        )
        results.append(f"{cls_uri},{inferred_classes_str}")
    return results