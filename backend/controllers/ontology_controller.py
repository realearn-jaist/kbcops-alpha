import os

from models.ontology_model import list_ontology, save_ontology

def upload_ontology(file, id):
    if id.endswith('.owl'):
        id = id[:-4]
    
    filename = id + '.owl'
    
    return save_ontology(file, id, filename)

def getAll_ontology():
    return list_ontology()

        

