def init_blueprints(app) -> None:
    from ml_serving.routes.prediction_routes import prediction_blueprint
    app.register_blueprint(prediction_blueprint)
