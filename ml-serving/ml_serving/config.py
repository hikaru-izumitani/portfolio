import logging
import os


class Config:

    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOGGING_LEVEL = logging.DEBUG
    MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:8080")
    TRACKING_URI = MLFLOW_TRACKING_URI
    MODELS = {
        "california-housing": {
            "1": {
                "model": None,
                "model_type": "REGRESSION",
                "mlflow_flavor": "sklearn",
                "explainer_path": "california-housing-explainer/1",
                "embedding_path": "california-housing-umap/1",
                "labels": None,
                "threshold": None,
            }
        }
    }
