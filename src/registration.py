import secrets
import string
import time, requests
from flask import (
    Blueprint,
    redirect,
    request,
    jsonify,
    render_template,
    request,
    url_for,
)
from datetime import datetime
from werkzeug.security import generate_password_hash

from src.models import Event, Participation, User, db

registration = Blueprint("registration", __name__)


def generate_random_password(length=8):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(alphabet) for _ in range(length))
    return password


@registration.route("/submit", methods=["POST"])
def submit_form():
    response_message = []
    existing_participation = None
    # Récupère les données du formulaire
    selected_date = request.form.get("date-select")
    names = request.form.getlist("name")
    lastnames = request.form.getlist("lastname")
    emails = request.form.getlist("email-input")

    event = Event.query.filter_by(date=selected_date).first()
    if not event:
        return "Événement non trouvé", 404

    total_names = len(names)

    remaining_slots = event.capacity - total_names

    if remaining_slots < 0:
        return jsonify(
            {
                "success": False,
                "message": "Il n'y a pas assez de places disponibles pour toutes les personnes.",
            }
        )

    for name, lastname, email in zip(names, lastnames, emails):
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            existing_participation = Participation.query.filter_by(
                event_id=event.id, user_id=existing_user.id
            ).first()
            if existing_participation:
                response_message.append(
                    f"Un utilisateur est déjà inscrit à cet événement avec cet email: {email}"
                )
                break
            else:
                user_id = existing_user.id

        else:
            random_password = generate_random_password()
            new_user = User(
                username=None,
                name=name,
                lastname=lastname,
                password=generate_password_hash(random_password, method="sha256"),
                email=email,
                role="Client",
            )
            db.session.add(new_user)
            db.session.flush()
            user_id = new_user.id

        if not existing_participation:
            participation = Participation(
                user_id=user_id, event_id=event.id, status=True
            )
            db.session.add(participation)

    db.session.commit()

    if response_message:
        return jsonify({"success": False, "message": "\n".join(response_message)})
    else:
        return jsonify({"success": True})


@registration.route("/success", methods=["GET"])
def success():
    # You can add any data you want to pass to the success.html template here
    return render_template("success.html")
