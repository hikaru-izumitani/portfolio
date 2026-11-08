from sqlalchemy import UniqueConstraint

from rest_api.services.database.database_client import db


class UserSQL(db.Model):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"),)

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
