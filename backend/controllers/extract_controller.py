from backend.models.extract_model import save_annotations, save_axioms, save_classes, save_individuals
from backend.models.ontology_model import getPath_ontology

from owl2vec_star.lib.Onto_Projection import Reasoner, OntologyProjection # type: ignore
from owl2vec_star.lib.Label import pre_process_words # type: ignore

def extract_data(id):
    onto_file = getPath_ontology(id)
    
    print(onto_file)
    
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
                    
    axioms = save_axioms(id, axioms)
    classes = save_classes(id, classes)
    individuals = save_individuals(id, individuals)
    annotations = save_annotations(id, annotations, projection)
    
    return {
        "no_class": len(classes), 
        "no_indiviual": len(individuals), 
        "no_axiom": len(axioms), 
        "no_annotation": len(annotations)
    }