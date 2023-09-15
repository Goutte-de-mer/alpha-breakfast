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


@main.route("/update-event", methods=["POST"])
def update_event():
    try:
        data = request.get_json()  # Utilisez get_json() pour récupérer les données JSON

        event_id = data.get("event_id")
        new_data = data.get("new_data")

        # Recherchez l'événement par son ID
        event = Event.query.get(event_id)

        if not event:
            return jsonify({"success": False, "message": "Événement non trouvé"})

        # Mettez à jour les champs de l'événement avec les nouvelles données
        for field_name, field_value in new_data.items():
            setattr(event, field_name, field_value)

        # Enregistrez les modifications en base de données
        db.session.commit()

        return jsonify({"success": True})
    except Exception as e:
        # En cas d'erreur lors de la mise à jour, annulez les modifications
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)})


# Route pour récupérer les détails de l'événement par ID
@main.route("/get-event/<int:event_id>", methods=["GET"])
def get_event(event_id):
    try:
        # Recherchez l'événement par son ID
        event = Event.query.get(event_id)

        if not event:
            return jsonify({"success": False, "message": "Événement non trouvé"})

        # Construisez un dictionnaire contenant les détails de l'événement
        event_details = {
            "date": event.date.strftime("%Y-%m-%d"),
            "capacity": event.capacity,
            "start_time": event.start_time,
            "duration": event.duration,
        }

        return jsonify({"success": True, "event": event_details})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
