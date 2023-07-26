from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configuration de la base de données MySQL
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:root@localhost:8889/db_alpha_breakfast"
# Vous pouvez également désactiver le suivi des modifications pour améliorer les performances (optionnel)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy(app)
