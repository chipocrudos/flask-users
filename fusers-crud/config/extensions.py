import logging
from asyncio import get_event_loop

from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from itsdangerous.url_safe import URLSafeTimedSerializer

from .config import Configuration

ma = Marshmallow()
db = SQLAlchemy()
mail = Mail()
loop = get_event_loop()

logger = logging.getLogger(__name__)

urlsafe = URLSafeTimedSerializer(Configuration.KEY_URL_TOKEN)

