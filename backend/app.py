from utils.file_handler import replace_or_create_folder
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.routes import ontology_blueprint
from routes.auth_routes import auth_blueprint, initialize_default_user
import os


def create_app():
    """function to create the Flask app and register the blueprints"""
    app = Flask(__name__, static_folder="../frontend/dist")
    CORS(app)
    
    # Configure JWT settings
    app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Change this to a secure key
    jwt = JWTManager(app)

    STORAGE_FOLDER = "storage"
    app.config["STORAGE_FOLDER"] = STORAGE_FOLDER

    app.register_blueprint(ontology_blueprint, url_prefix="/api")
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    @app.route("/")
    def serve():
        """function to serve the index.html file from the frontend folder"""
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/<path:path>")
    def static_proxy(path):
        """function to serve the static files from the frontend folder"""
        return send_from_directory(app.static_folder, path)
    
    # Initialize default user
    initialize_default_user(app.config["STORAGE_FOLDER"])

    return app

if __name__ == "__main__":
    """main function to run the Flask app"""
    app = create_app()
    app.run(debug=True)
