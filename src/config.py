import os

class Settings:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "DATA"))
    RAW_DIR = os.path.join(BASE_DIR, "raw")
    DATABASE_DIR = os.path.join(BASE_DIR, "database")

    AGRIBORA_CSV = os.path.join(RAW_DIR,"agribora_maize_prices.csv")
    KAMIS_RAW_CSV = os.path.join(RAW_DIR,"kamis_maize_prices_raw.csv")
    KAMIS_CSV = os.path.join(RAW_DIR, "kamis_maize_prices.csv")

settings = Settings()
