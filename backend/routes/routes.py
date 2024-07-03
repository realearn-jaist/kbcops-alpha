import time
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from utils.directory_utils import explore_directory, get_path, remove_dir, zip_files
from utils.json_handler import convert_float32_to_float
from utils.exceptions import handle_exception
from controllers.evaluator_controller import predict_func
from controllers.embed_controller import embed_func
from controllers.ontology_controller import (
    get_onto_stat,
    get_all_ontology,
    upload_ontology,
    extract_data,
)
from models.evaluator_model import read_evaluate, read_garbage_metrics
from models.graph_model import load_graph
from models.ontology_model import remove_row_ownership_csv, write_to_ownership_csv
from models.log_model import configure_logging

# create a blueprint for the ontology routes
ontology_blueprint = Blueprint("ontology", __name__)
logger = configure_logging()


@ontology_blueprint.route("/upload", methods=["POST"])
def upload():
    """Uploads an ontology file to the server and saves it in the storage folder"""
    try:
        if "owl_file" not in request.files:
            return jsonify({"message": "No file part"}), 400

        file = request.files["owl_file"]
        ontology_name = request.form.get("ontology_name")
        alias = request.form.get("alias")

        if file.filename == "":
            return jsonify({"message": "No selected file"}), 400

        if not ontology_name:
            return jsonify({"message": "No ontology name provided"}), 400

        ontology_name = upload_ontology(file, ontology_name)
        if ontology_name:
            write_to_ownership_csv(alias, ontology_name)
            logger.info(
                "File upload successful : {}".format(
                    [ontology_name, "with alias name :", alias]
                )
            )
            return (
                jsonify(
                    {
                        "message": "File uploaded successfully",
                        "ontology_name": ontology_name,
                    }
                ),
                200,
            )
        else:
            logger.error(
                "File upload failed : {}".format(
                    [ontology_name, "with alias name :", alias]
                )
            )
            remove_dir(get_path(ontology_name))
            return jsonify({"message": "File upload failed"}), 500

    except Exception as e:
        exception = handle_exception(e)
        return jsonify({"message": exception["message"]}), exception["error_code"]


@ontology_blueprint.route("/extract/<ontology>", methods=["GET"])
def extract(ontology):
    """Extracts the data from the ontology file and returns it as a JSON object"""
    try:
        start_time = time.time()
        data = extract_data(ontology)
        print(
            "---------------> time usage for extract {}: {} <---------------".format(
                ontology, time.time() - start_time
            )
        )
        if data:
            logger.info("Extraction successful : {}".format([ontology]))
            return (
                jsonify({"message": "Extraction successfully", "onto_data": data}),
                200,
            )
        else:
            logger.error("Extraction failed : {}".format([ontology]))
            remove_row_ownership_csv(ontology)
            remove_dir(get_path(ontology))
            return jsonify({"message": "Extraction failed"}), 500

    except Exception as e:
        exception = handle_exception(e)
        return jsonify({"message": exception["message"]}), exception["error_code"]


@ontology_blueprint.route("/ontology", methods=["GET"])
def list_ontologies():
    """Lists all the ontologies that have been uploaded to the server"""
    try:
        ontologies = get_all_ontology()
        logger.info("Ontologies listed successfully : {}".format(ontologies))
        return (
            jsonify(
                {"message": "Ontologies listed successfully", "onto_list": ontologies}
            ),
            200,
        )

    except Exception as e:
        exception = handle_exception(e)
        return jsonify({"message": exception["message"]}), exception["error_code"]


@ontology_blueprint.route("/ontology/<ontology>", methods=["GET"])
def get_ontology_stat(ontology):
    """Returns the statistics of the ontology file as a JSON object"""
    try:
        data = get_onto_stat(ontology)
        logger.info("Ontology Stats loaded successfully : {}".format([ontology]))
        return (
            jsonify(
                {"message": "load Ontologies Stats successfully", "onto_data": data}
            ),
            200,
        )

    except Exception as e:
        exception = handle_exception(e)
        return jsonify({"message": exception["message"]}), exception["error_code"]


@ontology_blueprint.route("/embed/<ontology>", methods=["GET"])
def embed_route(ontology):
    """Generates the embeddings for the ontology file using the specified algorithm"""
    try:
        algorithm = request.args.get("algo")
        print(f"Ontology: {ontology}, Algorithm: {algorithm}")

        start_time = time.time()
        result = embed_func(ontology_name=ontology, algorithm=algorithm)
        print(
            "---------------> time usage for embed {} with {}: {} <---------------".format(
                ontology, algorithm, time.time() - start_time
            )
        )

        print(result, f"{algorithm}")
        logger.info("Embed successful for {}".format([ontology, algorithm]))
        return (
            jsonify({"message": result, "ontology_name": ontology, "algo": algorithm}),
            200,
        )
    except Exception as e:
        logger.error("Embed failed for {}".format([ontology, algorithm]))
        remove_dir(get_path(ontology, algorithm))
        exception = handle_exception(e)
        return jsonify({"message": exception["message"]}), exception["error_code"]


@ontology_blueprint.route(
    "/evaluate/<ontology>/<algorithm>/<classifier>", methods=["GET"]
)
def predict_route(ontology, algorithm, classifier):
    """Evaluates the embeddings generated by the specified algorithm for the ontology file"""
    try:
        start_time = time.time()
        result = predict_func(
            ontology_name=ontology, algorithm=algorithm, classifier=classifier
        )
        result = convert_float32_to_float(result)
        print(
            "---------------> time usage for evaluate {} with {}: {} <---------------".format(
                ontology, algorithm, time.time() - start_time
            )
        )
        logger.info(
            "Evaluate successful for {}".format([ontology, algorithm, classifier])
        )
        return jsonify(result), 200

    except Exception as e:
        exception = handle_exception(e)
        logger.error("Evaluate failed for {}".format([ontology, algorithm, classifier]))
        remove_dir(get_path(ontology, algorithm, classifier))
        return jsonify({"message": exception["message"]}), exception["error_code"]


@ontology_blueprint.route(
    "/evaluate/<ontology>/<algorithm>/<classifier>/stat", methods=["GET"]
)
def get_evaluate_stat(ontology, algorithm, classifier):
    """Returns the evaluation statistics of the ontology file for the specified algorithm"""
    try:
        result = dict()
        result["message"] = "load evaluate successful!"
        result["performance"] = read_evaluate(ontology, algorithm, classifier)
        result["garbage"] = read_garbage_metrics(ontology, algorithm, classifier)
        result["images"] = load_graph(ontology, algorithm, classifier)
        logger.info(
            "Load Evaluate Stats loaded successfully for {}".format(
                [ontology, algorithm, classifier]
            )
        )
        return jsonify(result), 200

    except Exception as e:
        logger.error(
            "Load Evaluate Stats failed for {}".format(
                [ontology, algorithm, classifier]
            )
        )
        result["message"] = exception["message"]
        result["performance"] = {
            "mrr": 0,
            "hit_at_1": 0,
            "hit_at_5": 0,
            "hit_at_10": 0,
            "garbage": 0,
            "total": 0,
            "average_garbage_Rank": 0,
            "average_Rank": 0,
        }
        result["garbage"] = []
        result["images"] = []
        exception = handle_exception(e)
        return jsonify(result), exception["error_code"]


@ontology_blueprint.route("/explore", methods=["GET"])
def explore_directory_endpoint():
    """Explores the directory and returns its structure as a JSON object"""
    try:
        directory_path = current_app.config["STORAGE_FOLDER"]
        directory_structure = explore_directory(directory_path)
        logger.info(
            "Get files information successfully : {}".format(
                [i["name"] for i in directory_structure]
            )
        )
        return (
            jsonify(
                {
                    "message": "Get files information successfully",
                    "ontology": directory_structure,
                }
            ),
            200,
        )
    except Exception as e:
        exception = handle_exception(e)
        logger.error("Get files information failed : {}".format(str(e)))
        return jsonify({"message": exception["message"]}), exception["error_code"]


@ontology_blueprint.route("/explore/<ontology_name>", methods=["GET"])
def load_files(ontology_name):
    """Loads files related to a specific ontology and returns a zip file"""
    try:
        path = get_path(ontology_name)
        zip_hex = zip_files(path)

        response = {
            "message": "Zip file created successfully.",
            "file": zip_hex,  # Convert bytes to hex string for transmission
        }
        return jsonify(response), 200

    except Exception as e:
        exception = handle_exception(e)
        return jsonify({"message": exception["message"]}), exception["error_code"]


@ontology_blueprint.route("/explore/<ontology_name>", methods=["DELETE"])
@jwt_required()
def delete_file(ontology_name):
    """Deletes a file and its related data from the server"""
    try:
        path = get_path(ontology_name)

        if remove_dir(path):
            remove_row_ownership_csv(ontology_name)
            logger.info("File deleted successfully {}".format([ontology_name]))
            return jsonify({"message": "File deleted successfully"}), 200
        else:
            logger.info("File not found {}".format([ontology_name]))
            return jsonify({"message": "File not found"}), 404

    except Exception as e:
        exception = handle_exception(e)
        logger.error("File deletion failed {}".format([ontology_name]))
        return jsonify({"message": exception["message"]}), exception["error_code"]
