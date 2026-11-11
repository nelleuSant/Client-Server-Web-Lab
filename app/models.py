
from sqlalchemy import CheckConstraint
from app.extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(
        db.BigInteger,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        server_default="pending"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'completed')",
            name="valid_task_status"
        ),
    )
