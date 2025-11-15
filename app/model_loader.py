import joblib
from pathlib import Path
from src.config import settings

def load_saved_model():
    model_path = Path(settings.config["model"]["save_path"])
    scaler_path = Path(settings.config["model"]["scaler_path"])
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler
