
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.extensions import db
from app.models import Task

main = Blueprint("main", __name__)


# Serializa uma tarefa para JSON
def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }


# Página inicial
@main.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Client-Server Web Lab",
        "status": "running"
    }), 200


# Verificar aplicação
@main.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    }), 200


# Verificar banco de dados
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


# CREATE - Criar tarefa
@main.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON inválido ou ausente"}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "O título é obrigatório"}), 400

    if len(title.strip()) > 150:
        return jsonify({"error": "O título deve ter no máximo 150 caracteres"}), 400

    status = data.get("status", "pending")

    if status not in ["pending", "completed"]:
        return jsonify({"error": "Status inválido"}), 400

    task = Task(
        title=title.strip(),
        description=data.get("description"),
        status=status
    )

    try:
        db.session.add(task)
        db.session.commit()

        return jsonify(task_to_dict(task)), 201

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Não foi possível criar a tarefa"}), 500


# READ - Listar tarefas
@main.route("/api/tasks", methods=["GET"])
def list_tasks():
    tasks = db.session.execute(
        db.select(Task).order_by(Task.id)
    ).scalars().all()

    return jsonify([
        task_to_dict(task) for task in tasks
    ]), 200


# READ - Consultar tarefa específica
@main.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    return jsonify(task_to_dict(task)), 200


# UPDATE - Atualizar tarefa
@main.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON inválido ou ausente"}), 400

    if "title" in data:
        title = data["title"]

        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "O título não pode ser vazio"}), 400

        if len(title.strip()) > 150:
            return jsonify({"error": "O título deve ter no máximo 150 caracteres"}), 400

        task.title = title.strip()

    if "description" in data:
        task.description = data["description"]

    if "status" in data:
        if data["status"] not in ["pending", "completed"]:
            return jsonify({"error": "Status inválido"}), 400

        task.status = data["status"]

    task.updated_at = db.func.now()

    try:
        db.session.commit()
        return jsonify(task_to_dict(task)), 200

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Não foi possível atualizar a tarefa"}), 500


# DELETE - Excluir tarefa
@main.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    try:
        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "message": "Tarefa excluída com sucesso"
        }), 200

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Não foi possível excluir a tarefa"}), 500
