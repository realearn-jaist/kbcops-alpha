from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

auth_blueprint = Blueprint("auth", __name__)

# In-memory user store for example purposes. Use a database in a real app.
users = {
    "user@example.com": generate_password_hash("password")
}

@auth_blueprint.route("/signin", methods=["POST"])
def signin():
    email = request.json.get("email")
    password = request.json.get("password")

    if email not in users or not check_password_hash(users[email], password):
        return jsonify({"message": "Invalid credentials"}), 401

    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity=email, expires_delta=expires)
    return jsonify({"token": access_token}), 200
