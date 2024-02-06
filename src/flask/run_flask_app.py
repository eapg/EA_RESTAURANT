from flask import Flask
from src.flask.api_setup import setup_api

flask_app = Flask(__name__)


if __name__ == "__main__":
    app = setup_api(flask_app)
    app.run(debug=True)
