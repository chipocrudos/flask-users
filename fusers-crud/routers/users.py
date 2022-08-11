from flask import Blueprint
from views.users import (create_user_view, list_users_view,
                         me_update_user_view, me_view)

user_router = Blueprint("users", __name__, url_prefix="/users")

user_router.add_url_rule("/", view_func=list_users_view, methods=["GET"])
user_router.add_url_rule("/", view_func=create_user_view, methods=["POST"])

user_router.add_url_rule("/me/", view_func=me_view, methods=["GET"])
user_router.add_url_rule("/me/update/", view_func=me_update_user_view, methods=["PUT"])
