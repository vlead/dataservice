# -*- coding: utf-8 -*-

from flask import Flask, jsonify, make_response
from flask.ext.cors import CORS

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

    configure_errorhandlers(app)
    configure_cors(app)

    # all set; return app object
    return app


# configure cross origin resource sharing
def configure_cors(app):
    CORS(app)
    #CORS(app, origins=config.ALLOWED_ORIGINS,
    #     methods=['GET', 'OPTIONS', 'PUT', 'POST'], always_send=True)


# custom error handlers to return JSON errors with appropiate status codes
def configure_errorhandlers(app):

    @app.errorhandler(404)
    def not_found(err):
        return make_response(jsonify(error=err.description), 404)

    @app.errorhandler(400)
    def bad_request(err):
        return make_response(jsonify(error=err.description), 400)


if __name__ == "__main__":
    app = create_app(config)
    app.run(debug=True, host='0.0.0.0')
