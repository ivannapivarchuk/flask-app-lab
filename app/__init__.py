from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "super_secret_key"  # обов’язково для сесій та flash

    from .users.views import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    return app
