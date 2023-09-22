from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from email_validator import validate_email, EmailNotValidError
from src.models import User, db
from src.utils.misc import create_new_entry
from werkzeug.security import generate_password_hash

auth = Blueprint("auth", __name__)


# FUNCTIONS
def is_email(input_string):
    try:
        v = validate_email(input_string)
        return True
    except EmailNotValidError:
        return False


# ROUTES
@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    lastname = request.form.get("lastname")
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("L'adresse mail est déjà utilisée")
        return redirect(url_for("auth.signup"))

    encrypted_password = generate_password_hash(password, method="scrypt")

    create_new_entry(
        User,
        username=username,
        name=name,
        lastname=lastname,
        password=encrypted_password,
        email=email,
        role="admin",
    )

    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    login = request.form.get("login")
    password = request.form.get("password")

    if is_email(login):
        user = User.query.filter_by(email=login).first()
    else:
        user = user = User.query.filter_by(username=login).first()

    if not user or not check_password_hash(user.password, password):
        flash("Votre identifiant ou mot de passe est incorrect")
        return redirect(url_for("auth.login"))

    login_user(user)

    if user.role == "client":
        return redirect(url_for("main.client_account"))
    elif user.role == "admin":
        return redirect(url_for("main.admin_panel"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
