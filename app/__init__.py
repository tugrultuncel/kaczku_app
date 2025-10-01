import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config: dict | None = None) -> Flask:
    """Application factory for the Kaczku app."""
    app = Flask(__name__, instance_relative_config=False)

    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", "sqlite:///kaczku.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from . import models  # noqa: F401  # ensure models are registered

    @login_manager.user_loader
    def load_user(user_id: str):
        from .models import User

        if user_id and user_id.isdigit():
            return db.session.get(User, int(user_id))
        return None

    from .auth import auth_bp
    from .pins import pins_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pins_bp)

    with app.app_context():
        db.create_all()

    return app
