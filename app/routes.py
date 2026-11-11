from flask import Blueprint, jsonify
from sqlalchemy import text
from app.extensions import db

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


@main.route("/health/db", methods=["GET"])
def database_health():
    try:
        db.session.execute(text("SELECT 1"))

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except Exception:
        db.session.rollback()

        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 503
