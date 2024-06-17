import csv
import json
import os

from models.ontology_model import getPath_ontology_directory

def write_json_file(ontology, algorithm, data):
    
    file_path = os.path.join(getPath_ontology_directory(ontology), algorithm, "performance.json")
    
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        
def read_json_file(ontology, algorithm):
    
    file_path = os.path.join(getPath_ontology_directory(ontology), algorithm, "performance.json")
    
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def write_garbage_metrics(ontology, algorithm, data):
    json_output = []

    file_path = os.path.join(getPath_ontology_directory(ontology), algorithm, "garbage.csv")

    with open(file_path, 'w', newline='') as csv_file:
            column_names = list(data[0].keys())
            csv_writer = csv.DictWriter(csv_file, fieldnames=column_names)
            csv_writer.writeheader()
            csv_writer.writerows(data)
    
    return json_output

def read_garbage_metrics(ontology, algorithm):
    json_output = []

    headers = ['Individual', 'Predicted', 'Predicted_rank', 'True', 'True_rank', 
               'Score_predict', 'Score_true', 'Dif']
    
    file_path = os.path.join(getPath_ontology_directory(ontology), algorithm, "garbage.csv")

    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        for row in reader:
            row_dict = {headers[i]: row[i] for i in range(len(headers))}
            json_output.append(row_dict)
    
    return json_output