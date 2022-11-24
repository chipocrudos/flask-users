from config import cors, db, ma, mail, swagger
from flask import Flask
from handlers.errors import error_routes
from middleware.jwt_token import validate_token
from routers.routers import app_routes
from tools.app_function import cors_preflight_response, sync_db


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Configuration")

    ma.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    swagger.init_app(app)
    cors.init_app(app)

    app.before_first_request_funcs = [
        sync_db
    ]

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
        response.headers["Access-Control-Allow-Headers"] = (
                            "Content-Type,Authorization,"
                            "X-Requested-With,"
                            "x-csrf-token"
                        )
        response.headers["Access-Control-Allow-Methods"] = (
                            "GET, POST, OPTIONS, PUT, PATCH, DELETE")
        response.headers["Access-Control-Allow-Origin"] = app.config.get("ALLOW_ORIGIN")

        return response

    return app


if __name__ == "__main__":
    server = create_app()

    server.run(host="0.0.0.0")
