"""
Basic preprocessing: handle missing values, feature engineering, scaling.
"""

import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import joblib
from .config import settings

def load_raw(filepath):
    return pd.read_csv(filepath)

def prepare_timeseries(df):
    """
    Given raw FAOSTAT df, aggregate as needed and return features + target.
    Example: yearly features may be engineered from external datasets (rainfall, temp).
    For minimal pipeline, we use year as feature (and area/item) to predict yield_value.
    """
    df = df.copy()
    df = df.dropna(subset=["year", "yield_value"])
    # basic feature: year numeric, encode item & area if needed
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["yield_value"] = pd.to_numeric(df["yield_value"], errors="coerce")
    df = df.dropna(subset=["year", "yield_value"])

    # one-hot encode item/area if multiple present (small)
    df = pd.get_dummies(df, columns=["area", "item"], drop_first=True)

    X = df.drop(columns=["yield_value", "element"])
    y = df["yield_value"]
    return X, y

def fit_scaler(X, save_path=None):
    scaler = StandardScaler()
    scaler.fit(X)
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(scaler, save_path)
    return scaler

def scale_transform(X, scaler):
    return pd.DataFrame(scaler.transform(X), columns=X.columns, index=X.index)
