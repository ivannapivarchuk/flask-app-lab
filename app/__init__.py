from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.config import config


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.users.views import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    from app.posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix="/post")

    from app.products import products_bp
    app.register_blueprint(products_bp, url_prefix="/products")

    @app.route('/')
    def home():
        return render_template('resume.html', title="Резюме")

    @app.route('/contacts')
    def contacts():
        return render_template('contacts.html', title="Контакти")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app