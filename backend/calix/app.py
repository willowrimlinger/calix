from flask import Flask
from flask_migrate import Migrate

from calix.api.api import api
from calix.db import db


def create_app():
    app = Flask("calix")
    app.register_blueprint(api)
    Migrate(app, db)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
