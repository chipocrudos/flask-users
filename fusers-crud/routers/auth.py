from flask import Blueprint
from views.auth import (active_user_view, change_password_view, login_view,
                        password_recovery_view, registration_user_view)

auth_router = Blueprint("auth", __name__, url_prefix="/auth")

auth_router.add_url_rule("/login/", view_func=login_view, methods=["POST"])

auth_router.add_url_rule(
    "/register-user/", view_func=registration_user_view, methods=["POST"]
)

auth_router.add_url_rule("/active-user/<token>/", view_func=active_user_view, methods=["GET"])

auth_router.add_url_rule(
    "/password-recovery/", view_func=password_recovery_view, methods=["POST"]
)

auth_router.add_url_rule(
    "/change-password/<token>/", view_func=change_password_view, methods=["POST"]
)
