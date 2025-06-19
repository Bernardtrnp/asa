from flask import Flask, request, jsonify
import os
from .database import db
import datetime
from .config import (
    database_mongodb,
    database_mongodb_url,
)
from werkzeug.exceptions import BadRequest
import cloudinary
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    private_key_path = os.path.join(BASE_DIR, "keys", "private.pem")
    public_key_path = os.path.join(BASE_DIR, "keys", "public.pem")

    app.config.from_mapping(
        MONGODB_SETTINGS={
            "db": database_mongodb,
            "host": database_mongodb_url,
            "connect": False,
        },
    )

    global limiter
    limiter = Limiter(
        get_remote_address,
        app=app,
        storage_uri="redis://localhost:6379/0",
    )

    with open(private_key_path, "rb") as f:
        app.config["PRIVATE_KEY"] = f.read()

    with open(public_key_path, "rb") as f:
        app.config["PUBLIC_KEY"] = f.read()

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    cloudinary.config(
        secure=True,
        api_secret="_KGxUiymy5W6CJ955LQ6YWqaLKg",
        api_key="123149758941225",
        cloud_name="ducs7evff",
    )

    with app.app_context():
        from .api.login import login_router
        from .api.me import me_router
        from .api.testimoni import testimoni_router
        from .api.store_profile import store_profile_router
        from .api.api_key import api_key_router

        app.register_blueprint(login_router)
        app.register_blueprint(me_router)
        app.register_blueprint(testimoni_router)
        app.register_blueprint(store_profile_router)
        app.register_blueprint(api_key_router)

    @app.after_request
    async def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = (
            "Content-Type, Authorization, If-None-Match"
        )
        response.headers["Access-Control-Expose-Headers"] = "ETag"
        return response

    @app.before_request
    async def before_request():
        request.timestamp = datetime.datetime.now(datetime.timezone.utc)

    @app.errorhandler(BadRequest)
    async def handle_bad_request(e):
        return (
            jsonify(
                {
                    "message": str(e.description),
                }
            ),
            400,
        )

    @app.errorhandler(429)
    async def handle_too_many_requests(e):
        return (
            jsonify(
                {
                    "message": "too many requests",
                }
            ),
            429,
        )

    return app
