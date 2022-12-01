import logging
from asyncio import get_event_loop
from logging.config import dictConfig

from flasgger import Swagger
from flask_cors import CORS
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from itsdangerous.url_safe import URLSafeTimedSerializer

from .config import SWAGGER_CONFIG, Configuration

ma = Marshmallow()
db = SQLAlchemy()
mail = Mail()
cors = CORS()

swagger = Swagger(
    config=SWAGGER_CONFIG, merge=True, template_file=Configuration.TEMPLATE_FILE
)

loop = get_event_loop()

dictConfig(Configuration.LOGGING)
logger = logging.getLogger(__name__)

urlsafe = URLSafeTimedSerializer(Configuration.KEY_URL_TOKEN)
