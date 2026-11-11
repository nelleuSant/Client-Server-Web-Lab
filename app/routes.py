

from sqlalchemy import text
from app.extensions import db

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
