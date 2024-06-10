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
    result = embedAndPredict.embed_predict_func(
        ontology_file=f"./ontologies/foodon-merged.train.owl.owl",
        embedding_dir="./embeddings",
        config_file="default.cfg",
        algorithm=algorithm
    )
    
    return jsonify({"message": result})
