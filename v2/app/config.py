
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    PORTAL_NAME = os.getenv("PORTAL_NAME", "IntraHub")
    WELCOME_MESSAGE = os.getenv(
        "WELCOME_MESSAGE",
        "Welcome! Authenticate to continue."
    )

    PORTAL_SSID = os.getenv("PORTAL_SSID", "IntraHub-WiFi")

    PORTAL_PASSWORD_HASH = os.getenv("PORTAL_PASSWORD_HASH")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = (
        os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    )

    PERMANENT_SESSION_LIFETIME = 1800

    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_DEFAULT = "200 per day"
