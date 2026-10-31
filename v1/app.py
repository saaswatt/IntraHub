
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

PORTAL_PASSWORD = os.environ.get(
    "PORTAL_PASSWORD",
    "PortalTest123"
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>IntraHub</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #101b30;
            color: white;
            font-family: Arial, sans-serif;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 380px;
            text-align: center;
        }

        .wifi {
            font-size: 55px;
            margin-bottom: 25px;
        }

        h1 {
            font-size: 32px;
            margin-bottom: 8px;
        }

        p {
            color: #a9bdd6;
            margin-bottom: 30px;
        }

        input {
            width: 100%;
            padding: 16px;
            border: 1px solid #344765;
            border-radius: 10px;
            background: #26364f;
            color: white;
            font-size: 16px;
            margin-bottom: 15px;
        }

        button {
            width: 100%;
            padding: 16px;
            background: #1686dc;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .message {
            margin-top: 20px;
            color: #67d5ff;
        }

        footer {
            margin-top: 45px;
            color: #71849f;
            font-size: 12px;
        }
    </style>
</head>

<body>
    <div class="container">

        <div class="wifi">📶</div>

        <h1>Welcome!</h1>

        <p>
            Welcome to IntraHub.
            Enter your access password to continue.
        </p>

        <form method="POST">

            <input
                type="password"
                name="password"
                placeholder="Enter access password"
                required
            >

            <button type="submit">
                Connect to Internet
            </button>

        </form>

        {% if message %}
            <div class="message">{{ message }}</div>
        {% endif %}

        <footer>
            Powered by IntraHub
        </footer>

    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def portal():

    message = ""

    if request.method == "POST":

        password = request.form.get("password", "")

        if password == PORTAL_PASSWORD:
            message = "Authentication successful!"
        else:
            message = "Incorrect password. Try again."

    return render_template_string(
        HTML,
        message=message
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )
