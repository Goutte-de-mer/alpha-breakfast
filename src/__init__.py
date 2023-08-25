from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = "*2|Q#sd_1%6cOxop"

    # Configuration de la base de données MySQL
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "mysql+pymysql://root:root@localhost:8889/db_alpha_breakfast"

    # Vous pouvez également désactiver le suivi des modifications pour améliorer les performances (optionnel)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialisation de l'extension SQLAlchemy
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .registration import registration as registration_blueprint

    app.register_blueprint(registration_blueprint)

    return app
