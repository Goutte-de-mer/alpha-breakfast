from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configuration de la base de données MySQL
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "mysql+pymysql://root:root@localhost:8889/db_alpha_breakfast"

    # Vous pouvez également désactiver le suivi des modifications pour améliorer les performances (optionnel)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialisation de l'extension SQLAlchemy
    db.init_app(app)

    return app
