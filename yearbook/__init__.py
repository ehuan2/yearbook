from flask import Flask
from yearbook.config import Config

# creates the app
def create_app(config_class = Config):
    # creates it with the set configuration
    app = Flask(__name__)
    app.config.from_object(Config)

    # adds in the main routes
    from yearbook.main.routes import main

    app.register_blueprint(main)

    return app