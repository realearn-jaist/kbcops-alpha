from flask import Flask
from flask_cors import CORS
from backend.routes.routes import ontology_blueprint


def create_app():
    app = Flask(__name__)
    CORS(app)

    STORAGE_FOLDER = "backend\\storage"
    app.config["STORAGE_FOLDER"] = STORAGE_FOLDER

    app.register_blueprint(ontology_blueprint, url_prefix="/")

    return app


app = create_app()
