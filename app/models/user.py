from app.config.db import db
from uuid import uuid4

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.String(), primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), nullable=True, server_default=db.func.current_timestamp())
    updated_on = db.Column(db.DateTime(timezone=True), nullable=True, server_onupdate=db.func.current_timestamp())

    def __repr__(self):

        return f"<User {self.username}>"
