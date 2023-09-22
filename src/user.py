from flask import Blueprint, render_template
from flask_login import current_user, login_required
from src.models import User
from src.utils.misc import admin_required

user = Blueprint("user", __name__)


@user.route("/users/<user_type>")
@login_required
@admin_required
def users(user_type=None):
    clients = User.query.filter_by(role="client").all()
    employees = User.query.filter_by(role="admin").all()

    if user_type == "clients":
        data = clients
    elif user_type == "employees":
        data = employees
    else:
        data = None

    return render_template(
        "users.html", name=current_user.name, user_type=user_type, data=data
    )
