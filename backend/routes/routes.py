import time
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask import current_app, jsonify, request, Blueprint  # type: ignore

from models.evaluator_model import read_evaluate, read_garbage_metrics
from controllers.evaluator_controller import predict_func
from controllers.embed_controller import embed_func
from controllers.ontology_controller import (
    get_onto_stat,
    get_all_ontology,
    upload_ontology,
    extract_data,
)
from models.graph_model import load_graph
from models.ontology_model import get_path_ontology_directory
from utils.directory_utils import explore_directory, remove_dir, zip_files
from utils.json_handler import convert_float32_to_float


# create a blueprint for the ontology routes
ontology_blueprint = Blueprint("ontology", __name__)


@ontology_blueprint.route("/upload", methods=["POST"])
def upload():
    """Uploads an ontology file to the server and saves it in the storage folder"""
    if "owl_file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["owl_file"]
    ontology_name = request.form.get("ontology_name")

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if not ontology_name:
        return jsonify({"message": "No ontology name provided"}), 400

    ontology_name = upload_ontology(file, ontology_name)
    if ontology_name:
        return (
            jsonify({"message": "File uploaded successfully", "ontology_name": ontology_name}),
            200,
        )
    else:
        return jsonify({"message": "File upload failed"}), 500


@ontology_blueprint.route("/extract/<ontology>", methods=["GET"])
def extract(ontology):
    """Extracts the data from the ontology file and returns it as a JSON object"""
    start_time = time.time()
    data = extract_data(ontology)
    print(
        "---------------> time usage for extract {}: {} <---------------".format(
            ontology, time.time() - start_time
        )
    )
    if data:
        return jsonify({"message": "Extraction successfully", "onto_data": data}), 200
    else:
        return jsonify({"message": "Extraction failed"}), 500


@ontology_blueprint.route("/ontology", methods=["GET"])
def list_ontologies():
    """Lists all the ontologies that have been uploaded to the server"""
    ontologies = get_all_ontology()
    return (
        jsonify({"message": "Ontologies listed successfully", "onto_list": ontologies}),
        200,
    )


@ontology_blueprint.route("/ontology/<ontology>", methods=["GET"])
def get_ontology_stat(ontology):
    """Returns the statistics of the ontology file as a JSON object"""
    data = get_onto_stat(ontology)
    return (
        jsonify({"message": "load Ontologies Stats successfully", "onto_data": data}),
        200,
    )


@ontology_blueprint.route("/embed/<ontology>", methods=["GET"])
def embed_route(ontology):
    """Generates the embeddings for the ontology file using the specified algorithm"""
    algorithm = request.args.get("algo")
    print(f"Ontology: {ontology}, Algorithm: {algorithm}")

    # if not then call the embed_func to generate the model
    start_time = time.time()
    result = embed_func(ontology_name=ontology, algorithm=algorithm)
    print(
        "---------------> time usage for embed {} with {}: {} <---------------".format(
            ontology, algorithm, time.time() - start_time
        )
    )

    print(result, f"{algorithm}")
    return jsonify({"message": result, "onto_id": ontology, "algo": algorithm}), 200


@ontology_blueprint.route("/evaluate/<ontology>/<algorithm>/<classifier>", methods=["GET"])
def predict_route(ontology, algorithm, classifier):
    """Evaluates the embeddings generated by the specified algorithm for the ontology file"""
    start_time = time.time()
    result = predict_func(ontology_name=ontology, algorithm=algorithm, classifier=classifier)
    result = convert_float32_to_float(result)
    print(
        "---------------> time usage for evaluate {} with {}: {} <---------------".format(
            ontology, algorithm, time.time() - start_time
        )
    )
    return jsonify(result), 200


@ontology_blueprint.route("/evaluate/<ontology>/<algorithm>/<classifier>/stat", methods=["GET"])
def get_evaluate_stat(ontology, algorithm, classifier):
    """Returns the evaluation statistics of the ontology file for the specified algorithm"""
    result = dict()

    try:
        result["message"] = "load evaluate successful!"
        result["performance"] = read_evaluate(ontology, algorithm, classifier)
        result["garbage"] = read_garbage_metrics(ontology, algorithm, classifier)
        result["images"] = load_graph(ontology, algorithm, classifier)
        return jsonify(result), 200
    except:
        result["message"] = "load evaluate not successful!"
        result["performance"] = {
            "mrr": 0,
            "hit_at_1": 0,
            "hit_at_5": 0,
            "hit_at_10": 0,
            "garbage": 0,
            "total": 0,
            "average_garbage_Rank": 0,
            "average_Rank": 0
        }
        result["garbage"] = []
        result["images"] = []
        return jsonify(result), 500

@ontology_blueprint.route("/explore", methods=["GET"])
def explore_directory_endpoint():
    directory_path = current_app.config["STORAGE_FOLDER"]
    try:
        directory_structure = explore_directory(directory_path)
        return jsonify({"message": "Get files information successfully", "ontology": directory_structure}), 200
    except Exception as e:
        return jsonify({"message": "Get files information failed", "ontology": {}}), 500
    
@ontology_blueprint.route('/explore/<ontology_name>', methods=['GET'])
def load_files(ontology_name):
    path = get_path_ontology_directory(ontology_name)
    
    zip_hex = zip_files(path)
    
    # Prepare response headers
    response = {
        "message": "Zip file created successfully.",
        "file": zip_hex  # Convert bytes to hex string for transmission
    }

    return jsonify(response), 200

@ontology_blueprint.route("/explore/<ontology_name>", methods=["DELETE"])
@jwt_required()
def delete_file(ontology_name):
    try:
        # Assuming get_path_ontology_directory gets the full path to the ontology directory
        path = get_path_ontology_directory(ontology_name)
        
        if remove_dir(path):
            return jsonify({"message": "File deleted successfully"}), 200
        else:
            return jsonify({"message": "File not found"}), 404
    except Exception as e:
        return jsonify({"message": "File deletion failed", "error": str(e)}), 500
    
