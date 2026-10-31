
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import check_password_hash

from app.extensions import limiter


portal_bp = Blueprint("portal", __name__)


@portal_bp.route("/", methods=["GET"])
def index():
    return render_template(
        "login.html",
        portal_name=current_app.config["PORTAL_NAME"],
        welcome_message=current_app.config["WELCOME_MESSAGE"],
        is_authenticated=session.get("authenticated", False),
    )


@portal_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():

    password = request.form.get("password", "")

    password_hash = current_app.config["PORTAL_PASSWORD_HASH"]

    if check_password_hash(password_hash, password):

        # Prevent reuse of any previous session data.
        session.clear()

        session["authenticated"] = True
        session.permanent = True

        current_app.logger.info(
            "authentication_success ip=%s",
            request.remote_addr,
        )

        flash("Authentication successful!", "success")

    else:

        current_app.logger.warning(
            "authentication_failure ip=%s",
            request.remote_addr,
        )

        flash("Incorrect password. Please try again.", "error")

    return redirect(url_for("portal.index"))


@portal_bp.route("/logout", methods=["POST"])
def logout():

    session.clear()

    current_app.logger.info(
        "session_logout ip=%s",
        request.remote_addr,
    )

    flash("You have been disconnected.", "info")

    return redirect(url_for("portal.index"))
