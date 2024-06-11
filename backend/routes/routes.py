from flask import jsonify, render_template, request
from backend import app
from ..controller import embed


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/embed", methods=["POST"])
def embed_route():
    data = request.json
    ontology = data["ontology"]
    algorithm = data["algorithm"]
    print(f"Ontology: {ontology}, Algorithm: {algorithm}")
    result = embed.embed_func(ontology_file=ontology, algorithm=algorithm)
    return jsonify({"message": result})
