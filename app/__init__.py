from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config

# Ініціалізація розширень
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Підключення БД та міграцій
    db.init_app(app)
    migrate.init_app(app, db)

    # --- Реєстрація Blueprint'ів ---

    # 1. Користувачі (Users)
    from app.users.views import users_bp
    app.register_blueprint(users_bp, url_prefix="/users")

    # 2. Пости (Posts) - ТОЙ ЩО МИ ДОДАЛИ
    from app.posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix="/post")

    # -------------------------------

    # Тимчасові маршрути
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