from flask import jsonify, request

from ml_serving.models.prediction import Prediction
from ml_serving.services.database.database_client import db
from ml_serving.services.database.prediction_sql import PredictionSQL
from ml_serving.services.prediction_service import prediction_service


class PredictionController(object):
    @staticmethod
    def create_prediction(model_name, model_version) -> tuple[dict, int]:
        try:
            request_data = request.get_json(silent=True)
            if not isinstance(request_data, dict) or "features" not in request_data:
                raise ValueError("Invalid input data: features are required.")
            prediction = Prediction(features=request_data["features"])
            prediction = prediction_service.create_prediction(
                model_name=model_name,
                model_version=model_version,
                prediction=prediction,
            )
            body = prediction.to_dict()
            if prediction.label_numeric is not None:
                body["label"] = float(prediction.label_numeric)
            return jsonify(body), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except (KeyError, FileNotFoundError, LookupError):
            error_msg = f"Model '{model_name}' (version '{model_version}') was not found"
            return jsonify({"error": error_msg}), 404
        except Exception:
            return jsonify({"error": "An internal error occurred."}), 500

    def get_prediction(self, prediction_id: str) -> tuple[dict, int]:
        prediction = Prediction.from_prediction_sql(prediction_id)
        if not prediction:
            return jsonify({"error": "Prediction not found"}), 404
        return jsonify(prediction.to_dict()), 200

    @classmethod
    def get_prediction_sql(cls, id_: str) -> "PredictionSQL":
        return db.session.query(PredictionSQL).filter_by(id=id_).first()


prediction_controller = PredictionController()
