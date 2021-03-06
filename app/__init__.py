"""Initialize app."""
from flask import Flask
from flask_qrcode import QRcode
from flask_bootstrap import Bootstrap


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    bootstrap = Bootstrap(app)
    app.config.from_object('config.Config')
    app.config['RECAPTCHA_PUBLIC_KEY'] = 'iubhiukfgjbkhfvgkdfm'
    app.config['RECAPTCHA_PARAMETERS'] = {'size': '100%'}
    qrcode = QRcode(app)


    with app.app_context():
        # Import parts of our application
        from . import routes
        return app
