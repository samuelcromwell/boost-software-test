from flask import Flask
from flask_mailman import Mail

from app.config import Config

mail = Mail()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or Config)

    mail.init_app(app)

    from app.orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    return app
