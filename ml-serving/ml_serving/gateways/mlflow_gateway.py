import mlflow

from ml_serving.models.prediction import Model


class MLFlowGateway:
    def __init__(self):
        self.models = {}

    def init_app(self, app):
        mlflow.set_tracking_uri(app.config["MLFLOW_TRACKING_URI"])
        self.models = app.config["MODELS"]

        for model_name, versions in self.models.items():
            for version, model_config in versions.items():
                flavor = model_config.get("mlflow_flavor", model_config.get("flavor", "pyfunc"))
                uri = self._get_model_uri(model_name, version)
                self.models[model_name][version]["model"] = self._load_models(uri, flavor)

                explainer_path = model_config.get("explainer_path")
                if explainer_path:
                    self.models[model_name][version]["explainer"] = self._load_explainer(explainer_path)
                else:
                    self.models[model_name][version]["explainer"] = None

                embedding_path = model_config.get("embedding_path")
                if embedding_path:
                    self.models[model_name][version]["embedding"] = self._load_embedding(embedding_path)
                else:
                    self.models[model_name][version]["embedding"] = None

    def _get_model_uri(self, name, version):
        return f"models:/{name}/{version}"

    def _load_models(self, model_uri, flavor):
        if flavor == "pyfunc":
            return mlflow.pyfunc.load_model(model_uri)
        if flavor == "sklearn":
            return mlflow.sklearn.load_model(model_uri)
        raise ValueError(f"Invalid flavor: {flavor}")

    def _load_explainer(self, explainer_path):
        return mlflow.pyfunc.load_model(f"models:/{explainer_path}")

    def _load_embedding(self, embedding_path):
        return mlflow.pyfunc.load_model(f"models:/{embedding_path}")

    def get_model(self, name, version):
        model_ = self.models[name][version]
        model = Model(
            type=model_["model_type"],
            name=name,
            version=str(version),
            threshold=model_["threshold"],
        )
        model.model = model_["model"]
        model._model = model_["model"]
        model._explainer = model_.get("explainer")
        model._embedding = model_.get("embedding")
        return model


mlflow_gateway = MLFlowGateway()
