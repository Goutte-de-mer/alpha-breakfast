from functools import wraps

from flask_login import current_user
from src.models import Event, Participation, db
from sqlalchemy import func
from flask import url_for, redirect


# Function to calculate the remaining places of an event
def calculate_remaining_places(event_id):
    event = Event.query.get(event_id)

    total_capacity = event.capacity

    # Récupère le nombre total de participants pour la date selectionnée
    total_participants = (
        db.session.query(func.count(Participation.id))
        .join(Event)
        .filter(Event.id == event_id)
        .scalar()
    )

    # Calcul le nbr de places restantes
    remaining_places = total_capacity - total_participants

    return remaining_places


# Create the admin_required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        elif current_user.role != "admin":
            return redirect(url_for("main.client_account"))
        return f(*args, **kwargs)

    return decorated_function


# Add to database
def create_new_entry(model, **kwargs):
    new_entry = model(**kwargs)
    db.session.add(new_entry)
    db.session.flush()
    return new_entry
