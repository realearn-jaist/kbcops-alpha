import os
from flask import current_app # type: ignore

def save_axioms(id, axioms):
    STORAGE_FOLDER = current_app.config['STORAGE_FOLDER']
    path = os.path.join(STORAGE_FOLDER, id, "axioms.txt")
    
    with open( path, "w", encoding="utf-8" ) as f:
        for axiom in axioms:
            f.write("%s\n" % axiom)
    
    return axioms

def save_classes(id, classes):
    STORAGE_FOLDER = current_app.config['STORAGE_FOLDER']
    path = os.path.join(STORAGE_FOLDER, id, "classes.txt")
    
    with open( path, "w", encoding="utf-8" ) as f:
        for cl in classes:
            f.write("%s\n" % cl)
            
    return classes

def save_individuals(id, individuals):
    STORAGE_FOLDER = current_app.config['STORAGE_FOLDER']
    path = os.path.join(STORAGE_FOLDER, id, "individuals.txt")
    
    with open( path, "w", encoding="utf-8" ) as f:
        for individual in individuals:
            f.write("%s\n" % individual)
            
    return individuals

def save_annotations(id, annotations, projection):
    STORAGE_FOLDER = current_app.config['STORAGE_FOLDER']
    path = os.path.join(STORAGE_FOLDER, id, "annotations.txt")
    
    with open( path, "w", encoding="utf-8" ) as f:
        for e in projection.entityToPreferredLabels:
            for v in projection.entityToPreferredLabels[e]:
                f.write("%s preferred_label %s\n" % (e, v))
        for a in annotations:
            f.write("%s\n" % " ".join(a))
            
    with open(path, 'r', encoding="utf-8" ) as file:
        lines = file.readlines()
        return lines