from utils.file_handler import replace_or_create_folder
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.routes import ontology_blueprint
import os


def create_app():
    app = Flask(__name__, static_folder="../frontend/dist")
    CORS(app)

    STORAGE_FOLDER = "backend/storage"
    app.config["STORAGE_FOLDER"] = STORAGE_FOLDER

    app.register_blueprint(
        ontology_blueprint, url_prefix="/"
    )  # Assuming your API endpoints are under /api

    # Route for serving the index.html
    @app.route("/")
    def serve():
        return send_from_directory(app.static_folder, "index.html")

    # Route for serving other static files
    @app.route("/<path:path>")
    def static_proxy(path):
        return send_from_directory(app.static_folder, path)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
