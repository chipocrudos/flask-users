from flask import Flask

from config import db, logger, ma, mail
from middleware.jwt_token import validate_token
from routers.routers import app_routes


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Configuration")

    ma.init_app(app)
    db.init_app(app)
    mail.init_app(app)

    app.before_request_funcs = {
        "app.users": [validate_token]
    }

    app.register_blueprint(app_routes)

    @app.before_first_request
    def sync_db():
        logger.warning("Sync database")
        db.create_all(app=create_app())

    return app


if __name__ == "__main__":
    server = create_app()

    server.run(host="0.0.0.0")
