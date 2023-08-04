import time, requests
from datetime import datetime
from flask import redirect, render_template, jsonify, request, url_for
from models import breakfast, reservations, db
from src import create_app


app = create_app()


def calculate_remaining_places(breakfasts):
    dates_and_remaining_places = {}
    for b in breakfasts:
        total_people = (
            reservations.query.with_entities(db.func.sum(reservations.nbr_of_people))
            .filter_by(id_breakfast=b.id)
            .scalar()
        )
        if total_people is None:
            total_people = 0
        remaining_places = b.quota - total_people
        unix_timestamp = int(time.mktime(b.date.timetuple()))
        dates_and_remaining_places[str(unix_timestamp)] = remaining_places
    return dates_and_remaining_places


@app.route("/", methods=["GET"])
def index():
    # Get all breakfast dates and quotas
    breakfasts = breakfast.query.all()

    # Calculate the remaining places for each breakfast date
    dates_and_remaining_places = calculate_remaining_places(breakfasts)

    return render_template(
        "index.html", dates_and_remaining_places=dates_and_remaining_places
    )


@app.route("/data", methods=["GET"])
def get_data():
    # Get all breakfast dates and quotas
    breakfasts = breakfast.query.all()

    # Calculate the remaining places for each breakfast date
    dates_and_remaining_places = calculate_remaining_places(breakfasts)

    return jsonify(dates_and_remaining_places)


@app.route("/submit", methods=["POST"])
def submit_form():
    # Get the form data from the request
    name = request.form.get("name")
    lastname = request.form.get("lastname")
    email = request.form.get("email-input")
    people = int(request.form.get("people"))
    selected_date_timestamp = int(request.form.get("date-select"))

    # Convert the selected_date_timestamp to a date object
    selected_date = datetime.fromtimestamp(selected_date_timestamp).date()

    # Find the breakfast record associated with the selected date
    selected_breakfast = breakfast.query.filter_by(date=selected_date).first()

    # Check if there is any reservation with the same email for the selected date
    existing_reservation = reservations.query.filter_by(
        email=email, id_breakfast=selected_breakfast.id
    ).first()

    if existing_reservation:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Une réservation pour cette date a déjà été faite avec cette adresse mail",
                }
            ),
            200,
        )

    # Fetch all breakfast dates and quotas using the get_data endpoint
    response = requests.get(url_for("get_data", _external=True))
    dates_and_remaining_places = response.json()

    # Convert the selected_date to a string in the same format as the keys in dates_and_remaining_places
    selected_date_str = str(int(time.mktime(selected_date.timetuple())))

    # Check if the selected_date is in the dates_and_remaining_places data
    if selected_date_str in dates_and_remaining_places:
        remaining_places = int(dates_and_remaining_places[selected_date_str])
        if remaining_places < people:
            # If there are not enough remaining places, show an error message
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Pas assez de places restantes pour cette date",
                    }
                ),
                200,
            )

    # Create a new reservation and add it to the database
    reservation = reservations(
        name=name,
        lastname=lastname,
        email=email,
        nbr_of_people=people,
        id_breakfast=selected_breakfast.id,
    )
    db.session.add(reservation)
    db.session.commit()

    # If the reservation is successful, redirect to another template
    return jsonify({"success": True, "message": "Reservation successful"}), 200


@app.route("/success", methods=["GET"])
def success():
    # You can add any data you want to pass to the success.html template here
    return render_template("success.html")
