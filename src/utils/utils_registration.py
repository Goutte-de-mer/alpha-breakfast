import hashlib
import secrets
import string
from src.models import Participation, User, db
from src.utils.email import send_email
from werkzeug.security import generate_password_hash


# FUNCTIONS
def generate_random_password(length=8):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(alphabet) for _ in range(length))
    encrypted_password = generate_password_hash(password, method="scrypt")
    return encrypted_password


# Fonction pour générer un jeton unique
def generate_unique_token(email):
    random_string = secrets.token_hex(16)
    unique_key = email + random_string
    salt = secrets.token_bytes(16)
    token = hashlib.scrypt(
        unique_key.encode(), salt=salt, n=16384, r=8, p=1, maxmem=0
    ).hex()
    return token


def send_registration_email(email, selected_date, name, lastname, registration_link):
    variables = {
        "selected_date": selected_date,
        "lastname": lastname,
        "name": name,
        "email": email,
        "details_link": registration_link,
    }
    send_email(email, "Votre réservation", "info_reservation.html", variables)


def add_participation(existing_user, event):
    participation = Participation(
        user_id=existing_user.id, event_id=event.id, status=True
    )
    db.session.add(participation)
