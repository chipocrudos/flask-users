from config import db, logger
from config.config import Configuration
from flask import make_response, request


def sync_db():
    logger.warning("Sync database")
    db.create_all()


def cors_preflight_response():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers',
                                'Content-Type,Authorization,X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,OPTIONS,PUT,PATCH,DELETE')

        response.headers.add("Access-Control-Allow-Origin",
                                Configuration.ALLOW_ORIGIN)

        if 'Cache-Control' not in response.headers:
            response.headers['Cache-Control'] = 'no-cache'

        return response
