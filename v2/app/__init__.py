
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask

from app.config import Config
from app.extensions import csrf, limiter


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Validate mandatory security configuration
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY is missing. Configure it in the root .env file."
        )

    if not app.config.get("PORTAL_PASSWORD_HASH"):
        raise RuntimeError(
            "PORTAL_PASSWORD_HASH is missing. Configure it in the root .env file."
        )

    # Configure authentication event logging
    log_directory = Path(__file__).resolve().parent.parent / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)

    auth_log = RotatingFileHandler(
        log_directory / "auth.log",
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )

    auth_log.setLevel(logging.INFO)
    auth_log.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"
        )
    )

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(auth_log)

    # Initialize Flask extensions
    csrf.init_app(app)
    limiter.init_app(app)

    # Register application routes
    from app.routes import portal_bp

    app.register_blueprint(portal_bp)

    return app
