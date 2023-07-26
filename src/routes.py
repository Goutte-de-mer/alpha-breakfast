from models import breakfast
from src import app
from flask import render_template


@app.route("/", methods=["GET"])
def index():
    # Récupérez toutes les dates disponibles depuis la table "breakfast"
    dates = [str(b.date) for b in breakfast.query.all()]

    return render_template("index.html", dates=dates)
