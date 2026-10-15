"""A tiny Flask API used to practise Docker + CI/CD."""
import os
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "dev")


@app.route("/")
def home():
    return jsonify(message="Hello from my first DevOps project!", env=APP_ENV)


@app.route("/health")
def health():
    """Used by Docker HEALTHCHECK, load balancers and monitoring scripts."""
    return jsonify(status="ok", version=APP_VERSION)


@app.route("/time")
def current_time():
    return jsonify(utc=datetime.now(timezone.utc).isoformat())


if __name__ == "__main__":
    # Only for local runs. In Docker we use gunicorn.
    app.run(host="0.0.0.0", port=5000)
