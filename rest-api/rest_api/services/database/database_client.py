from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=BaseModel)


def init_db(app) -> None:
    import rest_api.services.database.user_sql

    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
