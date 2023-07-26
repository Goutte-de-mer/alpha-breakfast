from src import db


class breakfast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    quota = db.Column(db.Integer, nullable=False)


class reservations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_breakfast = db.Column(db.Integer, db.ForeignKey("breakfast.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    nbr_of_people = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
