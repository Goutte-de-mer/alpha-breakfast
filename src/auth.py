from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError

from src.models import User, db

auth = Blueprint("auth", __name__)


# FUNCTIONS
def is_email(input_string):
    try:
        v = validate_email(input_string)
        return True
    except EmailNotValidError:
        return False


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

    new_user = User(
        email=email,
        name=name,
        lastname=lastname,
        username=username,
        password=generate_password_hash(password, method="sha256"),
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/admin-login5049661")
def login():
    return render_template("login.html")


@auth.route("/admin-login5049661", methods=["POST"])
def login_post():
    login = request.form.get("login")
    password = request.form.get("password")

    if is_email(login):
        user = User.query.filter_by(email=login).first()
    else:
        user = user = User.query.filter_by(username=login).first()

    if not user or not check_password_hash(user.password, password):
        flash("Votre identifiant ou mot de passe est incorrect")
        return redirect(
            url_for("auth.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    login_user(user)
    return redirect(url_for("main.admin_panel"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))