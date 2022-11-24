from http import HTTPStatus

from flask import Blueprint, jsonify, make_response
from marshmallow.exceptions import ValidationError

error_routes = Blueprint("erros", __name__)


@error_routes.app_errorhandler(ValidationError)
def validation_error(err):
    return make_response(jsonify(err.messages), HTTPStatus.BAD_REQUEST)
