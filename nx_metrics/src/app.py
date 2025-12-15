import sentry_sdk
from core.film import film_bp
from core.user import user_bp
from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.register_blueprint(film_bp)
app.register_blueprint(user_bp)
ma = Marshmallow(app)


@app.route("/ping")
def health() -> tuple:
    return "Pong", 200


if __name__ == "__main__":
    app.run()
