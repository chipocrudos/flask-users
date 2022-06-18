from flask import Blueprint
from views.auth import login_view

auth_router = Blueprint("auth", __name__, url_prefix="/auth")

auth_router.add_url_rule("/login/", view_func=login_view, methods=["POST"])
