import sqlite3
from config import settings

def get_connection():
    """Return SQLite connection using path from .env"""
    conn = sqlite3.connect(settings.database_path, check_same_thread=False)
    return conn
