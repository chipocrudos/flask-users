from flask import Blueprint

from .auth import auth_router
from .users import user_router

app_routes = Blueprint("app", __name__, url_prefix="/api")

app_routes.register_blueprint(user_router)
app_routes.register_blueprint(auth_router)
