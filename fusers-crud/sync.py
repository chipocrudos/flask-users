from config.extensions import db
from main import create_app

db.create_all(app=create_app())
