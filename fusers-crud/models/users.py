from datetime import datetime

from config.extensions import db
from sqlalchemy import Boolean, Column, DateTime, Integer, String


class User(db.Model):

    id = Column(Integer, primary_key=True)
    email = Column(String(180), unique=True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    hashed_password = Column(String(500))
    date_create = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=False)
    is_super = Column(Boolean, default=False)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
