import time
from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy import func
from src.models import Event, Participation, db

main = Blueprint("main", __name__)


def calculate_remaining_places(selected_date):
    event = Event.query.filter_by(date=selected_date).first()

    total_capacity = event.capacity

    # Récupère le nombre total de participants pour la date selectionnée
    total_participants = (
        db.session.query(func.count(Participation.id))
        .join(Event)
        .filter(Event.date == selected_date)
        .scalar()
    )

    # Calcul le nbr de places restantes
    remaining_places = total_capacity - total_participants

    return remaining_places


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Récupère la capacité maximale de la date selectionnée
        selected_date = request.form.get("date-select")
        remaining_places = calculate_remaining_places(selected_date)
        return jsonify({"remainingPlaces": remaining_places})

    # Récupère les événements avec le statut "ouvert"
    opened_events = Event.query.filter_by(status="ouvert").all()

    # Créer un set de dates uniques
    dates = set(event.date for event in opened_events)

    return render_template("index.html", dates=dates)


@main.route("/admin-panel")
@login_required
def admin_panel():
    return render_template("adminpanel.html", name=current_user.name)
