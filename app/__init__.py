from flask import Flask

def create_app():
    app = Flask(__name__)

    from .users.views import users_bp
    from .products.views import products_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')

    return app
