import time
from flask import jsonify, render_template, request
from backend import app
from ..controller import embedAndPredict

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed_predict', methods=['POST'])
def embed_predict():
    data = request.json
    ontology = data['ontology']
    algorithm = data['algorithm']
    print(f"Ontology: {ontology}, Algorithm: {algorithm}")
    start_time = time.time()
    result = embedAndPredict.embed_predict_func(
        ontology_file="backend/ontologies/foodon-merged.train.owl",
        embedding_dir="backend/cache/output",
        config_file="backend/controller/default.cfg",
        algorithm=algorithm
    )
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")
    
    return jsonify({"message": result})
