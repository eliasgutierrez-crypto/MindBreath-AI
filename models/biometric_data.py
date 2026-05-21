# biometric_data.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class BiometricData(db.Model):

    __tablename__ = "biometric_data"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    state = db.Column(
        db.String(20),
        nullable=False
    )

    breathing_rate = db.Column(
        db.Integer,
        nullable=False
    )

    heart_rate = db.Column(
        db.Integer,
        nullable=False
    )

    movement = db.Column(
        db.Integer,
        nullable=False
    )

    stress_level = db.Column(
        db.String(20),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "state": self.state,
            "breathing_rate": self.breathing_rate,
            "heart_rate": self.heart_rate,
            "movement": self.movement,
            "stress_level": self.stress_level
        }