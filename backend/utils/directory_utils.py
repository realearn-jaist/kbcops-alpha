import csv
import io
import os
import shutil
from datetime import datetime
import zipfile
from flask import current_app
import numpy as np

def get_ontology_alias_mapping():
    directory_path = current_app.config["STORAGE_FOLDER"]
    csv_file = os.path.join(directory_path, "ownership.csv")
    
    ontology_alias_map = {}
    
    # Read alias mapping from ownership.csv
    if os.path.exists(csv_file):
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ontology_alias_map[row['ontology_name']] = row['alias']
    
    return ontology_alias_map

def get_file_info(path):
    """Return a dictionary with the file name and creation time."""
    return {
        "name": os.path.basename(path),
        "created_at": datetime.fromtimestamp(os.path.getctime(path)).isoformat()
    }

def explore_directory(directory):
    """Recursively explore the directory and return a structured JSON."""
    ontology_list = []
    ontology_alias_map = get_ontology_alias_mapping()
    
    for ontology_name in os.listdir(directory):
        ontology_path = os.path.join(directory, ontology_name)
        if os.path.isdir(ontology_path):
            ontology_info = {
                "name": ontology_name,
                "alias": ontology_alias_map.get(ontology_name, ""),  # Get alias if exists
                "created_at": datetime.fromtimestamp(os.path.getctime(ontology_path)).isoformat(),
                "process_files": [],
                "algorithm": []
            }
            
            for item in os.listdir(ontology_path):
                item_path = os.path.join(ontology_path, item)
                if os.path.isfile(item_path):
                    ontology_info["process_files"].append(get_file_info(item_path))
                elif os.path.isdir(item_path):
                    algo_info = {
                        "name": item,
                        "created_at": datetime.fromtimestamp(os.path.getctime(item_path)).isoformat(),
                        "process_files": [],
                        "classifier": []
                    }
                    
                    for algo_item in os.listdir(item_path):
                        algo_item_path = os.path.join(item_path, algo_item)
                        if os.path.isfile(algo_item_path):
                            algo_info["process_files"].append(get_file_info(algo_item_path))
                        elif os.path.isdir(algo_item_path):
                            classifier_info = {
                                "name": algo_item,
                                "created_at": datetime.fromtimestamp(os.path.getctime(algo_item_path)).isoformat(),
                                "process_files": [],
                                "graph_fig": []
                            }
                            
                            for classifier_item in os.listdir(algo_item_path):
                                classifier_item_path = os.path.join(algo_item_path, classifier_item)
                                if os.path.isfile(classifier_item_path):
                                    classifier_info["process_files"].append(get_file_info(classifier_item_path))
                                elif os.path.isdir(classifier_item_path):
                                    for graph_file in os.listdir(classifier_item_path):
                                        graph_file_path = os.path.join(classifier_item_path, graph_file)
                                        if os.path.isfile(graph_file_path):
                                            classifier_info["graph_fig"].append(get_file_info(graph_file_path))
                            
                            algo_info["classifier"].append(classifier_info)
                    
                    ontology_info["algorithm"].append(algo_info)
            
            ontology_list.append(ontology_info)
    
    return ontology_list

def zip_files(directory):
    # In-memory buffer to hold the zip file
    zip_buffer = io.BytesIO()

    # Create a zip file in memory
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))

    # Seek to the beginning of the buffer
    zip_buffer.seek(0)

    return zip_buffer.read().hex()

def remove_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        return directory
    else:
        return None