# -*- coding: utf-8 -*-

from flask import Flask
from db import db
from api import api

# import config file
import config


def create_app(config):
    # init our app
    app = Flask(__name__)

    # load config values from the config file
    app.config.from_object(config)

    # init sqlalchemy db instance
    db.init_app(app)
    db.app = app

    # register blueprints
    app.register_blueprint(api)

    # all set; return app object
    return app


if __name__ == "__main__":
    app = create_app(config)
    app.run(debug=True)
