# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler

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
    configure_logging(app)

    # all set; return app object
    return app


# configure cross origin resource sharing
def configure_cors(app):
    # CORS(app)
    CORS(app, origins=config.ALLOWED_ORIGINS,
         methods=['GET', 'OPTIONS', 'PUT', 'POST'])


# custom error handlers to return JSON errors with appropiate status codes
def configure_errorhandlers(app):

    @app.errorhandler(404)
    def not_found(err):
        if 'description' not in err:
            return make_response(jsonify(error='No such URL found'), 404)

        return make_response(jsonify(error=err.description), 404)

    @app.errorhandler(400)
    def bad_request(err):
        return make_response(jsonify(error=err.description), 400)


def configure_logging(app):
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                                  '[in %(pathname)s:%(lineno)d]')

    # Also error can be sent out via email. So we can also have a SMTPHandler?
    log_file = os.path.join(os.path.dirname(__file__), '..',
                            app.config['LOG_FILE'])

    max_size = 1024 * 1024 * 20  # Max Size for a log file: 20MB
    log_handler = RotatingFileHandler(log_file, maxBytes=max_size,
                                      backupCount=10)

    if 'LOG_LEVEL' in app.config:
        log_level = app.config['LOG_LEVEL'] or 'ERROR'
    else:
        log_level = 'ERROR'

    log_handler.setLevel(log_level)
    log_handler.setFormatter(formatter)

    app.logger.addHandler(log_handler)


if __name__ == "__main__":
    app = create_app(config)
    app.run(debug=True, host='0.0.0.0')
