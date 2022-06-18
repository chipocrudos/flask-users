from flask import Flask

from config.extensions import db, ma
from middleware.jwt_token import validate_token
from routers.routers import app_routes


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.config.Configuration")

    ma.init_app(app)
    db.init_app(app)

    app.before_request_funcs = {
        "app.users": [validate_token]
    }

    app.register_blueprint(app_routes)

    return app


if __name__ == "__main__":
    server = create_app()

    server.run()
