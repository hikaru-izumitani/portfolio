from flask import Blueprint

from ml_serving.controllers.prediction_controller import prediction_controller

prediction_blueprint = Blueprint("prediction", __name__)


@prediction_blueprint.route("/v1/<model_name>/version/<model_version>/predict", methods=["POST"])
def create_prediction(model_name, model_version):
    return prediction_controller.create_prediction(model_name, model_version)


@prediction_blueprint.route("/prediction/<id>", methods=["GET"])
def get_prediction(id: str):
    return prediction_controller.get_prediction(id)
