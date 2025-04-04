from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates, relationship
from sqlalchemy import ForeignKey
from . import db


class Hero(db.Model):
    __tablename__ = "heroes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = relationship(
        "HeroPower", backref="hero", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "hero_powers": [hp.to_dict() for hp in self.hero_powers],
        }


class Power(db.Model):
    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)

    hero_powers = relationship(
        "HeroPower", backref="power", cascade="all, delete-orphan"
    )

    @validates("description")
    def validate_description(self, key, value):
        if not value or len(value) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class HeroPower(db.Model):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, ForeignKey("heroes.id"), nullable=False)
    power_id = db.Column(db.Integer, ForeignKey("powers.id"), nullable=False)

    @validates("strength")
    def validate_strength(self, key, value):
        if value not in ["Strong", "Weak", "Average"]:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "strength": self.strength,
            "hero": {
                "id": self.hero.id,
                "name": self.hero.name,
                "super_name": self.hero.super_name,
            },
            "power": {
                "id": self.power.id,
                "name": self.power.name,
                "description": self.power.description,
            },
        }
