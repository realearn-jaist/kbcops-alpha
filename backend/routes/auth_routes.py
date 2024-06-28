import os
import json
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

auth_blueprint = Blueprint("auth", __name__)

def get_credentials():
    """Reads credentials from the JSON file."""
    credentials_path = os.path.join(current_app.config["STORAGE_FOLDER"], "admin_credential.json")
    if os.path.exists(credentials_path):
        with open(credentials_path, "r") as file:
            return json.load(file)
    return {}

def save_credentials(username, password_hash):
    """Saves the credentials to the JSON file."""
    credentials_path = os.path.join(current_app.config["STORAGE_FOLDER"], "admin_credential.json")
    with open(credentials_path, "w") as file:
        json.dump({"username": username, "password": password_hash}, file)

# Endpoint to update credentials (password)
@auth_blueprint.route("/update", methods=["POST"])
@jwt_required()
def update_credentials():
    current_username = get_jwt_identity()
    current_password = request.json.get("password")
    new_username = request.json.get("username")
    new_password = request.json.get("newPassword")
    
    if not current_password:
        return jsonify({"message": "Current password not provided"}), 400
    if not new_password:
        return jsonify({"message": "New password not provided"}), 400
    
    credentials = get_credentials()
    
    if current_username != credentials.get("username") or not check_password_hash(credentials.get("password"), current_password):
        return jsonify({"message": "Invalid current password"}), 401
    
    password_hash = generate_password_hash(new_password)
    save_credentials(new_username, password_hash)
    return jsonify({"message": "Credentials updated successfully"}), 200

# Endpoint to get the username associated with the current JWT token
@auth_blueprint.route("/username", methods=["GET"])
@jwt_required()
def get_username():
    current_username = get_jwt_identity()
    return jsonify({"username": current_username}), 200

# Sign-in endpoint
@auth_blueprint.route("/signin", methods=["POST"])
def signin():
    username = request.json.get("username")
    password = request.json.get("password")

    credentials = get_credentials()

    if username != credentials.get("username") or not check_password_hash(credentials.get("password"), password):
        return jsonify({"message": "Invalid credentials"}), 401

    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity=username, expires_delta=expires)
    return jsonify({"token": access_token}), 200

# Function to initialize the default user
def initialize_default_user(directory):
    credentials_path = os.path.join(directory, "admin_credential.json")
    if not os.path.exists(credentials_path):
        default_username = "admin"
        default_password_hash = generate_password_hash("password")
        
        with open(credentials_path, "w") as file:
            json.dump({"username": default_username, "password": default_password_hash}, file)
