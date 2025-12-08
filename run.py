import os
from app import create_app

# Обираємо конфігурацію (development за замовчуванням)
config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)

if __name__ == '__main__':
    app.run()