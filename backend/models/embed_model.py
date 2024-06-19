import os
import joblib
import gensim

from utils.file_handler import replace_or_create_folder
from models.ontology_model import getPath_ontology, getPath_ontology_directory

def isModelExist(ontology_name, algorithm):
    # check if system have ontology file and algorithm so that it can directly return the result
    path = os.path.join(getPath_ontology_directory(ontology_name), algorithm, "model")
    
    return os.path.exists(path)

def save_model(ontology_name, algorithm, model):
    path = os.path.join(getPath_ontology_directory(ontology_name), algorithm)
    
    replace_or_create_folder(path)
    
    path = os.path.join(path, "model")
    if algorithm == "rdf2vec":
        joblib.dump(model, path)
    else:
        model.save(path)
        
def load_model(ontology_name, algorithm):
    if not isModelExist(ontology_name, algorithm):
        return None
    
    path = os.path.join(getPath_ontology_directory(ontology_name), algorithm, "model")
    
    if algorithm == "rdf2vec":
        return joblib.load(path)
    else:
        return gensim.models.Word2Vec.load(path)
    # else:
    #     return gensim.models.word2vec.Word2Vec.load(path)
    
    