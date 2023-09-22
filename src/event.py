from flask_login import current_user, login_required
from src.models import Participation, Event, db
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from src.utils.email import send_cancellation_emails
from src.utils.misc import admin_required, create_new_entry


event = Blueprint("event", __name__)


# FONCTIONS


def delete_event_and_participations(event):
    Participation.query.filter_by(event_id=event.id).delete()
    db.session.delete(event)
    db.session.commit()


# Fonction pour vérifier le statut de l'événement et gérer les courriels d'annulation si nécessaire
def check_and_handle_event_status_change(event, new_data):
    if "status" in new_data:
        new_status_value = new_data["status"]
        current_status = event.status
        participations = Participation.query.filter_by(event_id=event.id).all()
        if new_status_value == "annule" and participations:
            send_cancellation_emails(event, participations)
            for participation in participations:
                participation.status = False
        elif current_status == "annule" and new_status_value == "ouvert":
            for participation in participations:
                participation.status = True


@event.route("/delete-event/<int:event_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        # Vérifie s'il y a des participations associées à cet événement
        participations = Participation.query.filter_by(event_id=event.id).all()

        if participations:
            # Envoie des e-mails d'annulation aux participants si des participations existent
            send_cancellation_emails(event, participations)

        # Supprime l'événement avec toutes ses participations
        delete_event_and_participations(event)

        return (
            jsonify(
                {
                    "message": "Événement et participations associées supprimés avec succès"
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "Événement non trouvé"}), 404


@event.route("/update-event", methods=["POST"])
@login_required
@admin_required
def update_event():
    try:
        data = request.get_json()  # Utilisez get_json() pour récupérer les données JSON

        event_id = data.get("event_id")
        new_data = data.get("new_data")

        # Recherchez l'événement par son ID
        event = Event.query.get(event_id)

        if not event:
            return jsonify({"success": False, "message": "Événement non trouvé"})

        check_and_handle_event_status_change(event, new_data)

        # Mets à jour les champs de l'événement avec les nouvelles données
        for field_name, field_value in new_data.items():
            setattr(event, field_name, field_value)

        db.session.commit()

        return jsonify({"success": True})
    except Exception as e:
        # En cas d'erreur lors de la mise à jour, annulez les modifications
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)})


# Route pour récupérer les détails de l'événement par ID
@event.route("/get-event/<int:event_id>", methods=["GET"])
@login_required
@admin_required
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


# Route pour afficher les participants d'un événement par son ID
@event.route("/participants/<int:event_id>")
@login_required
@admin_required
def show_participants(event_id):
    event = Event.query.get(event_id)

    if event:
        participants = Participation.query.filter_by(event_id=event.id).all()
        for participant in participants:
            print(participant.user.name)
        return render_template(
            "participants.html",
            event=event,
            participants=participants,
            name=current_user.name,
        )
    else:
        # Gérez le cas où l'événement n'existe pas
        return "Événement non trouvé", 404


@event.route("/new-event")
@login_required
@admin_required
def new_event():
    return render_template("create_event.html", name=current_user.name)


@event.route("/create-event", methods=["POST"])
@login_required
@admin_required
def create_event():
    response_message = []
    # Comptez le nombre d'événements avant la création
    number_of_events_before = Event.query.count()
    # Données du formulaire
    title = request.form.get("event-title")
    description = request.form.get("description")
    date = request.form.get("date")
    start_time = request.form.get("start-time")
    duration = request.form.get("duration")
    capacity = request.form.get("capacity")
    status = request.form.get("event-status")

    existing_date = Event.query.filter_by(date=date).first()

    create_new_entry(
        Event,
        title=title,
        description=description,
        date=date,
        start_time=start_time,
        duration=duration,
        capacity=capacity,
        status=status,
    )

    db.session.commit()

    # Comptez à nouveau le nombre d'événements après la création
    number_of_events_after = Event.query.count()

    if number_of_events_after < number_of_events_before:
        response_message.append("Un problème a eu lieu avec la création de l'événement")
        return jsonify({"success": False, "message": "\n".join(response_message)})
    else:
        response_message.append("L'événement créé avec succès &#128521;")
        return jsonify({"success": True})
