import os
import time
from controllers import embed
from controllers.extract_controller import extract_data
from flask import jsonify, request, Blueprint  # type: ignore
from controllers.ontology_controller import getAll_ontology, upload_ontology


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

    path = upload_ontology(file, id)
    if path:
        return (
            jsonify({"message": "File uploaded successfully", "onto_id": id[:-4]}),
            200,
        )
    else:
        return jsonify({"message": "File upload failed"}), 500


@ontology_blueprint.route("/extract/<ontology>", methods=["GET"])
def extract(ontology):
    if ontology.endswith(".owl"):
        ontology = ontology[:-4]

    data = extract_data(ontology)
    if data:
        return jsonify({"message": "Extraction successfully", "data": data}), 200
    else:
        return jsonify({"message": "Extraction failed"}), 500


@ontology_blueprint.route("/ontology", methods=["GET"])
def list_ontologies():
    ontologies = getAll_ontology()
    return (
        jsonify({"message": "Ontologies listed successfully", "onto_list": ontologies}),
        200,
    )


# @ontology_blueprint.route('/embed-predict', methods=['GET'])
# def embed_predict():
#     data = request.json
#     ontology = data['ontology']
#     algorithm = data['algorithm']
#     print(f"Ontology: {ontology}, Algorithm: {algorithm}")
#     start_time = time.time()
#     result = embedAndPredict.embed_predict_func(
#         ontology_file="backend/ontologies/foodon-merged.train.owl",
#         embedding_dir="backend/cache/output",
#         config_file="backend/controller/default.cfg",
#         algorithm=algorithm
#     )
#     end_time = time.time()

#     execution_time = end_time - start_time
#     print(f"Execution time: {execution_time} seconds")


#     return jsonify({"message": result})
@ontology_blueprint.route("/embed/<ontology>", methods=["GET"])
def embed_route(ontology):

    algorithm = request.args.get('algo')
    print(f"Ontology: {ontology}, Algorithm: {algorithm}")
    # result = embed.embed_func(ontology_file=ontology, algorithm=algorithm)
    return jsonify({"message": 0})
