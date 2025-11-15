"""
Evaluate saved model on holdout data or full dataset.
"""

import joblib
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from .config import settings
from .preprocessing import prepare_timeseries, scale_transform

def evaluate_model(raw_csv_path=None, model_path=None, scaler_path=None):
    cfg = settings.config
    raw_csv_path = raw_csv_path or f"{cfg['data']['raw_path']}/{settings.crop}_{settings.country}_yield_{settings.start_year}_{settings.end_year}.csv"
    model_path = model_path or cfg["model"]["save_path"]
    scaler_path = scaler_path or cfg["model"]["scaler_path"]

    df = pd.read_csv(raw_csv_path)
    X, y = prepare_timeseries(df)
    scaler = joblib.load(scaler_path)
    Xs = scale_transform(X, scaler)

    model = joblib.load(model_path)
    preds = model.predict(Xs)

    rmse = mean_squared_error(y, preds, squared=False)
    r2 = r2_score(y, preds)

    return {"rmse": rmse, "r2": r2, "n_samples": len(y)}

if __name__ == "__main__":
    print(evaluate_model())
