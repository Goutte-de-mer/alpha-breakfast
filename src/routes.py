from flask import render_template
from models import breakfast, reservations
from src import create_app

app = create_app()


@app.route("/", methods=["GET"])
def index():
    # Get all breakfast dates and quotas
    breakfasts = breakfast.query.all()

    # Calculate the remaining places for each breakfast date
    dates_and_remaining_places = {}
    for b in breakfasts:
        total_people = reservations.query.filter_by(id_breakfast=b.id).count()
        remaining_places = b.quota - total_people
        dates_and_remaining_places[b.date.strftime("%d-%m-%Y")] = remaining_places

    return render_template(
        "index.html", dates_and_remaining_places=dates_and_remaining_places
    )
