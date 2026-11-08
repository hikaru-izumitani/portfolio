from flask import Flask

from rest_api.routes.user_routes import user_blueprint
from rest_api.services.database.database_client import init_db


def create_app(test_config=None):
    app = Flask(__name__)

    from rest_api.config import Config

    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    init_db(app)
    app.register_blueprint(user_blueprint)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
