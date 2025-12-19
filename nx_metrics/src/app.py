import sentry_sdk
from core.film import film_bp
from core.user import user_bp
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(film_bp)
app.register_blueprint(user_bp)
ma = Marshmallow(app)

CORS(
    app,
    resources={r"/*": {"origins": "http://localhost:4200"}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "OPTIONS"],
)


@app.route("/ping")
def health() -> tuple:
    return "Pong", 200


if __name__ == "__main__":
    app.run()
