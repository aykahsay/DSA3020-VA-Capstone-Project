"""
Train a regression model (Random Forest) and save model + scaler.
"""

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

from .config import settings
from .preprocessing import prepare_timeseries, fit_scaler, scale_transform

def train_pipeline(raw_csv_path=None):
    cfg = settings.config
    raw_csv_path = raw_csv_path or os.path.join(cfg["data"]["raw_path"],
                                                f"{settings.crop}_{settings.country}_yield_{settings.start_year}_{settings.end_year}.csv")
    df = pd.read_csv(raw_csv_path)

    X, y = prepare_timeseries(df)

    # simple train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=cfg["model"]["test_size"], random_state=cfg["project"]["random_state"]
    )

    # scale
    scaler_path = cfg["model"]["scaler_path"]
    scaler = fit_scaler(X_train, save_path=scaler_path)
    X_train_s = scale_transform(X_train, scaler)
    X_test_s = scale_transform(X_test, scaler)

    # model
    model = RandomForestRegressor(
        n_estimators=cfg["model"]["n_estimators"],
        max_depth=cfg["model"]["max_depth"],
        random_state=cfg["project"]["random_state"]
    )
    model.fit(X_train_s, y_train)

    # eval
    preds = model.predict(X_test_s)
    rmse = mean_squared_error(y_test, preds, squared=False)
    r2 = r2_score(y_test, preds)

    # save
    os.makedirs(os.path.dirname(cfg["model"]["save_path"]), exist_ok=True)
    joblib.dump(model, cfg["model"]["save_path"])
    joblib.dump(scaler, scaler_path)

    return {"rmse": rmse, "r2": r2, "model_path": cfg["model"]["save_path"], "scaler_path": scaler_path}

if __name__ == "__main__":
    print(train_pipeline())
