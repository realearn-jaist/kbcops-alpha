from utils.file_handler import replace_or_create_folder
from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.routes import ontology_blueprint
import os


def create_app():
    """function to create the Flask app and register the blueprints"""
    app = Flask(__name__, static_folder="../frontend/dist")
    CORS(app)

    STORAGE_FOLDER = "storage"
    app.config["STORAGE_FOLDER"] = STORAGE_FOLDER

    app.register_blueprint(ontology_blueprint, url_prefix="/")

    @app.route("/")
    def serve():
        """function to serve the index.html file from the frontend folder"""
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/<path:path>")
    def static_proxy(path):
        """function to serve the static files from the frontend folder"""
        return send_from_directory(app.static_folder, path)

    return app


if __name__ == "__main__":
    """main function to run the Flask app"""
    app = create_app()
    app.run(debug=True)
