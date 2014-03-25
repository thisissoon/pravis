# -*- coding: utf-8 -*-

"""
.. module:: pravis.app
    :synopsis: Flask application factory pattern:
               http://flask.pocoo.org/docs/patterns/appfactories/
"""

import os

from flask import Flask
from flask.ext.security import SQLAlchemyUserDatastore
from pravis.auth.models import User, Role
from pravis.ext import db, migrate, security, xmlrpc
from werkzeug import SharedDataMiddleware


def load_config(app, override=None):
    """
    Load application configuration from default module then overriding
    by environment variables

    :param app: Flask application instance
    :type app: flask.app.Flask
    """

    # Default configuration
    app.config.from_object('pravis.config.default')

    # Override using os environment variable
    if os.environ.get('PRAVIS_SETTINGS_PATH'):
        app.config.from_envvar('PRAVIS_SETTINGS_PATH')

    # If override path is supplied use those settings
    if override:
        app.config.from_pyfile(override)


def register_blueprints(app):
    """
    Load blueprints from config, similar to the INSALLED_APPS
    setting in Django

    :param app: Flask application instance
    :type app: flask.app.Flask
    """

    for blueprint in app.config['BLUEPRINTS']:

        module = None

        # Register Blueprints
        try:
            module = __import__(
                '{0}'.format(blueprint),
                fromlist=['pravis'])

            # Add routes
            for route, view in module.routes:
                module.blueprint.add_url_rule(
                    route,
                    view_func=view)

            # Register blueprint
            app.register_blueprint(module.blueprint)

        except ImportError:
            # TODO: Warning here
            pass
        except AttributeError:
            pass
            # TODO: Warning here

        # Import models
        try:
            __import__('{0}.models'.format(blueprint))
        except ImportError:
            pass


def register_extenstions(app):
    """
    Load flask extensions

    :param app: Flask application instance
    :type app: flask.app.Flask
    """

    # Database (Flask-SQLAlchemy)
    db.init_app(app)

    # Migrations
    migrate.init_app(app, db)

    # Flask Security
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore)

    # XMLRPC
    from pravis.simple.xmlrpc import search
    xmlrpc.connect(app, '/simple/')
    xmlrpc.register(search, 'search')


def create_app():
    """
    Bootstrap flask application
    """

    # Initialize Flask Application
    app = Flask(__name__)

    # Load Configuration
    load_config(app)

    # Initialize extensions
    register_extenstions(app)

    # Dynamically load blueprints
    register_blueprints(app)

    # Upload - only in debug
    if app.config['DEBUG']:
        app.add_url_rule(
            '/uploads/<filename>',
            'uploads',
            build_only=True)
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/uploads':  app.config['UPLOAD_DIR']
        })

    return app
