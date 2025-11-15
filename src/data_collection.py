"""
Fetch FAOSTAT crop data and save raw csv.
"""

import os
import requests
import pandas as pd
from .config import settings

def fetch_faostat_crop(crop=None, country=None, year_start=None, year_end=None, save_csv=True):
    crop = crop or settings.crop or settings.config["data"]["crop"]
    country = country or settings.country or settings.config["data"]["country"]
    year_start = year_start or settings.start_year
    year_end = year_end or settings.end_year

    base = settings.faostat_base_url or settings.config.get("faostat_base_url") or "https://fenixservices.fao.org/faostat/api/v1/en"
    # FAOSTAT QA/Crops or QCL/production endpoints vary; using QA/Crops where available
    # Example endpoint used earlier: /QA/Crops
    endpoint = f"{base}/QA/Crops"

    params = {
        "item": crop,
        "element": "Yield",     # yield element
        "area": country,
        "year": f"{year_start},{year_end}"
    }

    resp = requests.get(endpoint, params=params, timeout=30)
    resp.raise_for_status()
    j = resp.json()

    if "data" not in j:
        raise ValueError("Unexpected FAOSTAT response: no 'data' field")

    df = pd.DataFrame(j["data"])

    # normalize columns: keep year, area, item, element, value
    # FAOSTAT responses can include many fields; select safest subset
    for col in ["year", "area", "item", "value", "element"]:
        if col not in df.columns:
            df[col] = None

    df = df[["year", "area", "item", "element", "value"]].rename(columns={"value": "yield_value"})
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    # persist
    raw_dir = settings.config["data"]["raw_path"]
    os.makedirs(raw_dir, exist_ok=True)
    out = os.path.join(raw_dir, f"{crop}_{country}_yield_{year_start}_{year_end}.csv")
    if save_csv:
        df.to_csv(out, index=False)

    return df

if __name__ == "__main__":
    df = fetch_faostat_crop()
    print(df.head())
