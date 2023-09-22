from dotenv import load_dotenv
from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user, login_required
from src.models import Event, db
from src.utils.misc import calculate_remaining_places, admin_required

main = Blueprint("main", __name__)

load_dotenv()


# ROUTES
@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Récupère la capacité maximale de la date selectionnée
        event_id = request.form.get("date-select")
        remaining_places = calculate_remaining_places(event_id)
        return jsonify({"remainingPlaces": remaining_places})

    # Récupère les événements avec le statut "ouvert"
    opened_events = Event.query.filter_by(status="ouvert").all()

    return render_template("index.html", opened_events=opened_events)


@main.route("/admin-panel")
@login_required
@admin_required
def admin_panel():
    events = Event.query.all()
    remaining_places = calculate_remaining_places
    return render_template(
        "adminpanel.html",
        name=current_user.name,
        events=events,
        calculate_remaining_places=remaining_places,
    )


@main.route("/client-account")
@login_required
def client_account():
    return render_template("clientaccount.html", name=current_user.name)
