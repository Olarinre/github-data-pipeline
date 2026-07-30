# app/config.py

from pathlib import Path

from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _get_setting(name, default):
    value = os.getenv(name, default)
    if value is None:
        return default
    if isinstance(value, str):
        value = value.strip()
    return value or default


DATABASE_CONFIG = {
    "user": _get_setting("POSTGRES_USER", "postgres"),
    "password": _get_setting("POSTGRES_PASSWORD", "postgres"),
    "host": _get_setting("POSTGRES_HOST", "localhost"),
    "port": _get_setting("POSTGRES_PORT", "5432"),
    "database": _get_setting("POSTGRES_DB", "github_pipeline"),
}

DATABASE_URL = (
    f"postgresql+psycopg2://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)
print(DATABASE_URL)