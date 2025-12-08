import os

# Визначаємо базову директорію (де лежить цей файл)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Секретний ключ для сесій (беремо з середовища або дефолтний)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ivanna-secret-key-2024'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Шлях до БД: instance/data.sqlite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '../instance/data.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # База в пам'яті для тестів
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '../instance/data.sqlite')

# Словник для зручного імпорту
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}