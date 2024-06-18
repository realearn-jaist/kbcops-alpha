import os

from models.ontology_model import getPath_ontology_directory # type: ignore

def save_axioms(id, axioms):
    path = os.path.join(getPath_ontology_directory(id), "axioms.txt")
    
    with open( path, "w", encoding="utf-8" ) as f:
        for axiom in axioms:
            f.write("%s\n" % axiom)
    
    return axioms

def save_classes(id, classes):
    path = os.path.join(getPath_ontology_directory(id), "classes.txt")
    
    with open( path, "w", encoding="utf-8" ) as f:
        for cl in classes:
            f.write("%s\n" % cl)
            
    return classes

def save_individuals(id, individuals):
    path = os.path.join(getPath_ontology_directory(id), "individuals.txt")
    
    with open( path, "w", encoding="utf-8" ) as f:
        for individual in individuals:
            f.write("%s\n" % individual)
            
    return individuals

def save_annotations(id, annotations, projection):
    path = os.path.join(getPath_ontology_directory(id), "annotations.txt")
    
    with open( path, "w", encoding="utf-8" ) as f:
        for e in projection.entityToPreferredLabels:
            for v in projection.entityToPreferredLabels[e]:
                f.write("%s preferred_label %s\n" % (e, v))
        for a in annotations:
            f.write("%s\n" % " ".join(a))
            
    with open(path, 'r', encoding="utf-8" ) as file:
        lines = file.readlines()
        return lines
    
def load_axioms(id):
    path = os.path.join(getPath_ontology_directory(id), "axioms.txt")
    
    with open( path, "r", encoding="utf-8" ) as f:
        return f.readlines()

def load_classes(id):
    path = os.path.join(getPath_ontology_directory(id), "classes.txt")
    
    with open( path, "r", encoding="utf-8" ) as f:
        return set(f.readlines())

def load_individuals(id):
    path = os.path.join(getPath_ontology_directory(id), "individuals.txt")
    
    with open( path, "r", encoding="utf-8" ) as f:
        return set(f.readlines())

def load_annotations(id):
    path = os.path.join(getPath_ontology_directory(id), "annotations.txt")
    
    with open( path, "r", encoding="utf-8" ) as f:
        return f.readlines()
    
def save_infer(id, infers):
    path = os.path.join(getPath_ontology_directory(id), "inferred_ancestors.txt")
    
    with open( path, "w", encoding="utf-8" ) as f:
        for result in infers:
            f.write(result + "\n")
            
    return infers