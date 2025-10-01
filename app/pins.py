from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from . import db
from .models import Pin


pins_bp = Blueprint("pins", __name__)


@pins_bp.route("/")
@login_required
def map_view():
    return render_template("pins/map.html")


@pins_bp.route("/pins", methods=["GET"])
@login_required
def list_pins():
    pins = Pin.query.order_by(Pin.created_at.desc()).all()
    return jsonify([pin.to_dict() for pin in pins])


@pins_bp.route("/pins", methods=["POST"])
@login_required
def create_pin():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip() or None
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    errors: list[str] = []

    if not title:
        errors.append("Title is required.")
    if latitude is None or longitude is None:
        errors.append("Latitude and longitude are required.")

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except (TypeError, ValueError):
        errors.append("Latitude and longitude must be numbers.")

    if errors:
        return jsonify({"errors": errors}), 400

    pin = Pin(
        title=title,
        description=description,
        latitude=latitude,
        longitude=longitude,
        owner=current_user,
    )
    db.session.add(pin)
    db.session.commit()

    return jsonify(pin.to_dict()), 201
