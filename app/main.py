import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from src.config import settings
from src.preprocessing import prepare_timeseries
from src.utils import load_model

# Load model & scaler
MODEL_PATH = Path(settings.config["model"]["save_path"])
SCALER_PATH = Path(settings.config["model"]["scaler_path"])

@st.cache_resource
def load_artifacts():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

model, scaler = load_artifacts()

st.title("Crop Yield Prediction (Demo)")

st.markdown(f"**Crop:** {settings.crop}  •  **Country:** {settings.country}")

st.header("Predict yield (manual input)")

# For simplicity expect model features: year + optional dummy columns
year = st.number_input("Year", min_value=1980, max_value=2050, value=2025)
# Additional inputs: since feature set varies, keep a simple demonstrator:
area_input = st.text_input("Area (optional)", value=settings.country)

if st.button("Predict"):
    # Build a minimal DataFrame matching training columns: year and one-hot for area/item if used
    input_df = pd.DataFrame({"year": [year]})
    # If model expects dummy columns those must be added — here we attempt minimal approach
    try:
        # scale & predict
        X_scaled = scaler.transform(input_df)
        pred = model.predict(X_scaled)[0]
        st.success(f"Predicted yield: {pred:.2f}")
    except Exception as e:
        st.error("Model expects a different set of features. Re-run training to match this interface.")
        st.write(str(e))

st.header("Load sample data")
raw_path = Path(settings.config["data"]["raw_path"]) / f"{settings.crop}_{settings.country}_yield_{settings.start_year}_{settings.end_year}.csv"
if raw_path.exists():
    st.write(pd.read_csv(raw_path).head())
else:
    st.info("No raw CSV found. Run data collection first.")
