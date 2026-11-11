
from flask import Blueprint, jsonify

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Client-Server Web Lab",
        "status": "running"
    }), 200

@main.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    }), 200
