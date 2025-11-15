import os
import yaml
from dotenv import load_dotenv
from types import SimpleNamespace

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # repo/src -> repo

# load config.yaml
cfg_path = os.path.join(BASE_DIR, "config.yaml")
with open(cfg_path, "r") as f:
    _cfg = yaml.safe_load(f)

# combine .env and yaml into settings
settings = SimpleNamespace(
    # env
    faostat_base_url=os.getenv("FAOSTAT_BASE_URL"),
    database_path=os.getenv("DATABASE_PATH"),
    crop=os.getenv("CROP"),
    country=os.getenv("COUNTRY"),
    start_year=int(os.getenv("START_YEAR", _cfg["data"]["start_year"])),
    end_year=int(os.getenv("END_YEAR", _cfg["data"]["end_year"])),
    # yaml
    config=_cfg
)
