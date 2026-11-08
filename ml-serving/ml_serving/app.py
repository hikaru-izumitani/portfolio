from flask import Flask, jsonify

from ml_serving.gateways import mlflow_gateway
from ml_serving.routes import init_blueprints
from ml_serving.services.database.database_client import init_db


def create_app():
    app = Flask(__name__)

    from ml_serving.config import Config

    app.config.from_object(Config)
    init_db(app)

    @app.route("/")
    def index():
        return jsonify({"message": "Hello World!"})

    init_blueprints(app)
    mlflow_gateway.mlflow_gateway.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
