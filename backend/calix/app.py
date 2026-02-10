from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

import calix.models.__imports__
from calix.api.api import api
from calix.db import db


def create_app():
    app = Flask("calix")
    load_dotenv()
    app.config.from_prefixed_env("CALIX")
    print(app.config)
    app.register_blueprint(api)
    Migrate(app, db)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
