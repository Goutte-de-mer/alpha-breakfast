from src.utils.utils_registration import (
    generate_random_password,
    generate_unique_token,
    send_registration_email,
    add_participation,
)
from src.utils.misc import create_new_entry
from src.utils.email import is_valid_email
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, render_template, request
from src.models import Event, Participation, User, db

registration = Blueprint("registration", __name__)
load_dotenv()


# ROUTES
@registration.route("/submit", methods=["POST"])
def submit_form():
    response_message = []

    # Récupère les données du formulaire
    selected_date = request.form.get("date-select")
    names = request.form.getlist("name")
    lastnames = request.form.getlist("lastname")
    emails = request.form.getlist("email-input")

    event = Event.query.filter_by(id=selected_date).first()
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
        if not is_valid_email(email):
            response_message.append(f"L'adresse e-mail n'est pas valide : {email}")
            break
        elif len(name) > 30 or len(lastname) > 30:
            response_message.append(f"Nom ou prénom trop long")
            break

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            unique_token = existing_user.token
            # Si un utilisateur avec ce mail existe déjà, cherche s'il est déjà inscrit à cet événement
            existing_participation = Participation.query.filter_by(
                event_id=event.id, user_id=existing_user.id
            ).first()
            if existing_participation:
                response_message.append(
                    f"Un utilisateur est déjà inscrit à cet événement avec cet email: {email}"
                )
                break

        else:
            random_password = generate_random_password()
            unique_token = generate_unique_token(email)
            new_user = create_new_entry(
                User,
                name=name,
                lastname=lastname,
                email=email,
                password=random_password,
                role="client",
                token=unique_token,
            )
            existing_user = new_user

        registration_link = f"http://127.0.0.1:5000/details-reservation/{unique_token}"
        add_participation(existing_user, event)
        send_registration_email(email, selected_date, name, lastname, registration_link)

        db.session.commit()

    if response_message:
        return jsonify({"success": False, "message": "\n".join(response_message)})
    else:
        return jsonify({"success": True})


@registration.route("/success", methods=["GET"])
def success():
    return render_template("success.html")


@registration.route("/details-reservation/<unique_token>")
def user_reservation_details(unique_token):
    # Récupère l'utilisateur correspondant au jeton unique
    user = User.query.filter_by(token=unique_token).first()

    if user:
        # Récupère les participations de l'utilisateur
        participations = Participation.query.filter_by(user_id=user.id).all()

        event_info = []
        for participation in participations:
            event = Event.query.get(participation.event_id)
            if event:
                event_info.append(
                    {
                        "title": event.title,
                        "description": event.description,
                        "date": event.date,
                        "start_time": event.start_time,
                        "capacity": event.capacity,
                        "status": participation.status,
                    }
                )

        return render_template(
            "details_inscriptions.html", user=user, events=event_info
        )
    else:
        return "Utilisateur non trouvé", 404
