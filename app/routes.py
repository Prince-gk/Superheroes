from flask import Blueprint, jsonify, request
from .models import Hero, Power, HeroPower
from . import db

api = Blueprint("api", __name__)


@api.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify(
        [{"id": h.id, "name": h.name, "super_name": h.super_name} for h in heroes]
    )


@api.route("/heroes/<int:id>", methods=["GET"])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    return jsonify(
        {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "hero_powers": [
                {
                    "id": hp.id,
                    "hero_id": hp.hero_id,
                    "power_id": hp.power_id,
                    "strength": hp.strength,
                    "power": {
                        "id": hp.power.id,
                        "name": hp.power.name,
                        "description": hp.power.description,
                    },
                }
                for hp in hero.hero_powers
            ],
        }
    )


@api.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return jsonify(
        [{"id": p.id, "name": p.name, "description": p.description} for p in powers]
    )


@api.route("/powers/<int:id>", methods=["GET"])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(
        {"id": power.id, "name": power.name, "description": power.description}
    )


@api.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    new_description = data.get("description")

    if not new_description or len(new_description) < 20:
        return jsonify(
            {"errors": ["Description must be at least 20 characters long"]}
        ), 400

    power.description = new_description
    db.session.commit()

    return jsonify(
        {"id": power.id, "name": power.name, "description": power.description}
    )


@api.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.get_json()
    strength = data.get("strength")
    hero_id = data.get("hero_id")
    power_id = data.get("power_id")

    if strength not in ["Strong", "Weak", "Average"]:
        return jsonify(
            {"errors": ["Strength must be 'Strong', 'Weak', or 'Average'"]}
        ), 400

    try:
        new_hp = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
        db.session.add(new_hp)
        db.session.commit()

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        return jsonify(
            {
                "id": new_hp.id,
                "hero_id": hero.id,
                "power_id": power.id,
                "strength": new_hp.strength,
                "hero": {
                    "id": hero.id,
                    "name": hero.name,
                    "super_name": hero.super_name,
                },
                "power": {
                    "id": power.id,
                    "name": power.name,
                    "description": power.description,
                },
            }
        ), 201

    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


@api.route("/hero_powers/<int:id>", methods=["DELETE"])
def delete_hero_power(id):
    hero_power = HeroPower.query.get(id)
    if not hero_power:
        return jsonify({"error": "HeroPower not found"}), 404

    db.session.delete(hero_power)
    db.session.commit()

    return jsonify({"message": "HeroPower deleted successfully"}), 200
