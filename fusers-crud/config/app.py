from os import sync

from flask import Flask
from handlers.errors import error_routes
from middleware.jwt_token import validate_token
from routers.routers import app_routes
from tools.app_function import cors_preflight_response, sync_db

from . import TEMPLATE_FOLDER, cors, db, ma, mail, swagger


def create_app(config_object="config.Configuration"):

    app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

    app.config.from_object(config_object)

    ma.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    swagger.init_app(app)
    cors.init_app(app)

    app.before_first_request_funcs = [sync_db]

    app.before_request_funcs = {
        "app.users": [
            cors_preflight_response,
            validate_token,
        ]
    }

    app.register_blueprint(app_routes)
    app.register_blueprint(error_routes)

    @app.after_request
    def _after_request_header(response):
        if "Cache-Control" not in response.headers:
            response.headers["Cache-Control"] = "no-cache"

        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers[
            "Access-Control-Allow-Headers"
        ] = "Content-Type,Authorization, X-Requested-With, x-csrf-token"
        response.headers[
            "Access-Control-Allow-Methods"
        ] = "GET, POST, OPTIONS, PUT, PATCH, DELETE"
        response.headers["Access-Control-Allow-Origin"] = app.config.get("ALLOW_ORIGIN")

        return response

    return app
