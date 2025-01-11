import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")


def get_env():
    return {
        "postgres_user": os.getenv("POSTGRES_USER"),
        "postgres_password": os.getenv("POSTGRES_PASSWORD"),
        "postgres_server": os.getenv("POSTGRES_SERVER"),
        "postgres_db": os.getenv("POSTGRES_DB"),
    }
