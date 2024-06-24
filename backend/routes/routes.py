import time
from models.evaluator_model import read_evaluate, read_garbage_metrics
from controllers.graph_controller import create_graph
from controllers.evaluator_controller import predict_func
from controllers.embed_controller import embed_func
from flask import jsonify, request, Blueprint  # type: ignore
from controllers.ontology_controller import get_onto_stat, get_all_ontology, upload_ontology, extract_data
from models.graph_model import load_graph


ontology_blueprint = Blueprint("ontology", __name__)


@ontology_blueprint.route("/upload", methods=["POST"])
def upload():
    if "owl_file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["owl_file"]
    id = request.form.get("onto_id")

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if not id:
        return jsonify({"message": "No id provided"}), 400

    onto_id = upload_ontology(file, id)
    if onto_id:
        return (
            jsonify({"message": "File uploaded successfully", "onto_id": onto_id}),
            200,
        )
    else:
        return jsonify({"message": "File upload failed"}), 500


@ontology_blueprint.route("/extract/<ontology>", methods=["GET"])
def extract(ontology):
    start_time = time.time()
    data = extract_data(ontology)
    print("---------------> time usage for extract {}: {} <---------------".format(ontology, time.time() - start_time))
    if data:
        return jsonify({"message": "Extraction successfully", "onto_data": data}), 200
    else:
        return jsonify({"message": "Extraction failed"}), 500


@ontology_blueprint.route("/ontology", methods=["GET"])
def list_ontologies():
    ontologies = get_all_ontology()
    return (
        jsonify({"message": "Ontologies listed successfully", "onto_list": ontologies}),
        200,
    )
    
@ontology_blueprint.route("/ontology/<ontology>", methods=["GET"])
def get_ontology_stat(ontology):
    data = get_onto_stat(ontology)
    return (
        jsonify({"message": "Ontologies listed successfully", "onto_data": data}),
        200,
    )
    

@ontology_blueprint.route("/embed/<ontology>", methods=["GET"])
def embed_route(ontology):
    algorithm = request.args.get("algo")
    print(f"Ontology: {ontology}, Algorithm: {algorithm}")

    # if not then call the embed_func to generate the model
    start_time = time.time()
    result = embed_func(ontology_name=ontology, algorithm=algorithm)
    print("---------------> time usage for embed {} with {}: {} <---------------".format(ontology, algorithm, time.time() - start_time))
    
    print(result, f"{algorithm}")
    return jsonify({"message": result, "onto_id": ontology, "algo": algorithm}), 200


@ontology_blueprint.route("/evaluate/<ontology>/<algorithm>", methods=["GET"])
def predict_route(ontology, algorithm):
    start_time = time.time()
    result = predict_func(ontology_name=ontology, algorithm=algorithm)
    print("---------------> time usage for evaluate {} with {}: {} <---------------".format(ontology, algorithm, time.time() - start_time))
    return jsonify(result), 200

@ontology_blueprint.route("/evaluate/<ontology>/<algorithm>/stat", methods=["GET"])
def get_evaluate_stat(ontology, algorithm):
    result = dict()
    
    try:
        result["message"] = "load evaluate successful!"
        result["performance"] = read_evaluate(ontology, algorithm)
        result["garbage"] = read_garbage_metrics(ontology, algorithm)
        result["images"] = load_graph(ontology, algorithm)
        return jsonify(result), 200
    except:
        result["message"] = "load evaluate not successful!"
        result["performance"] = {"mrr": 0, "hit_at_1": 0, "hit_at_5": 0, "hit_at_10": 0, "garbage": 0 }
        result["garbage"] = []
        result["images"] = []
        return jsonify(result), 500