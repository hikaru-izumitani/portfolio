# California Housing Model Serving

A Flask API that loads a California Housing regression model from MLflow, returns the prediction together with SHAP values and a 3D UMAP embedding, and stores the result in SQLite.

## Tested Environments

- macOS 27.2
  - Python 3.14

## Project Structure

```text
ml-serving/
├── register_models.py
├── requirements.txt
├── ml_serving/
│   ├── app.py
│   ├── config.py
│   ├── controllers/
│   ├── gateways/
│   ├── models/
│   ├── routes/
│   └── services/
└── tests/
```

## Requirements

- Python 3.11 or newer
- The packages in `requirements.txt`

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/hikaru-izumitani/portfolio.git
cd portfolio/ml-serving
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Start a new MLflow server

Use an empty SQLite file. The first registered version of each model is then version 1, which is what `ml_serving/config.py` loads.

```bash
mlflow server --port 8080 --backend-store-uri sqlite:///mlruns.db
```

If port 8080 is already in use, pick another port and set `MLFLOW_TRACKING_URI` to that address before the next two commands. For example:

```bash
export MLFLOW_TRACKING_URI=http://127.0.0.1:8081
```

### 4. Register the model, explainer, and embedding

In a second terminal, from `portfolio/ml-serving`:

```bash
source .venv/bin/activate
python register_models.py
```

The script trains a decision tree on the California Housing data, then registers:

- `california-housing` version 1
- `california-housing-explainer` version 1
- `california-housing-umap` version 1

Registration fits a UMAP model, so this step takes a few minutes.

### 5. Start the API

```bash
python -m ml_serving.app
```

The API listens on `http://127.0.0.1:5000`.

### 6. Request a prediction

```bash
curl -s -X POST http://127.0.0.1:5000/v1/california-housing/version/1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "MedInc": 8.3252,
      "HouseAge": 41.0,
      "AveRooms": 6.984127,
      "AveBedrms": 1.02381,
      "Population": 322.0,
      "AveOccup": 2.555556,
      "Latitude": 37.88,
      "Longitude": -122.23
    }
  }'
```

The response includes:

- `label`: the predicted median house value, in units of $100,000
- `shap_values`: one number per input feature
- `embeddings`: a 3D UMAP projection of the input, with `x`, `y`, and `z`
- `id`: the stored prediction id

Fetch that stored prediction with:

```bash
curl -s http://127.0.0.1:5000/prediction/<id>
```

A request without `features` returns 400. An unknown model name or version returns 404.

### 7. Run the tests

The tests use a stand-in model, so MLflow does not need to be running.

```bash
pytest
```

## What this demonstrates

- Loading a registered scikit-learn model from MLflow
- Serving a regression prediction from a Flask API
- Returning SHAP values for that prediction
- Returning a persisted 3D UMAP embedding of the input
- Storing the prediction, SHAP values, and embedding in SQLite
- Rejecting missing features, an unknown model, and a failed explanation or embedding
- pytest coverage of the prediction path

## Reproducibility

`mlruns.db` and the API database are created locally and are not stored in the repository.

Start the MLflow server with a new SQLite file. Running `register_models.py` again on the same server creates version 2, and the API still requests version 1. Delete `mlruns.db` and register once to get back to version 1.

The API database is `instance/data.db`. Predictions saved there remain available after a restart.
