from models import breakfast
from flask import render_template
from src import create_app
from datetime import datetime

app = create_app()


@app.route("/", methods=["GET"])
def index():
    # Récupérez toutes les dates disponibles depuis la table "breakfast"
    dates = [
        datetime.strptime(str(b.date), "%Y-%m-%d").strftime("%d-%m-%Y")
        for b in breakfast.query.all()
    ]

    return render_template("index.html", dates=dates)
