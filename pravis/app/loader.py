# -*- coding: utf-8 -*-

"""
.. module:: pravis.app.loader
    :synopsis: Helper utilities for application factory, mostly utilities
               around auto loading blueprints, models and admin registration.
"""

import os

from flask.ext.security import SQLAlchemyUserDatastore
from pravis.auth.models import User, Role
from pravis.app.ext import admin, db, migrate, security, xmlrpc
from pravis.exceptions import ImproperlyConfigured
from werkzeug import SharedDataMiddleware


def load_config(app, override=None):
    """
    Load application configuration from default module then overriding
    by environment variables

    :param app: Flask application instance
    :type app: flask.app.Flask

    :param override: Optional path to a settings file
    :type override: str
    """

    # Default configuration
    app.config.from_object('pravis.config.default')

    # Override using os environment variable
    if os.environ.get('PRAVIS_SETTINGS_PATH'):
        app.config.from_envvar('PRAVIS_SETTINGS_PATH')

    # If override path is supplied use those settings
    if override:
        app.config.from_pyfile(override)


def load_models(blueprint):
    """
    Load models from models.py of the blueprint module if it exist.

    :param blueprint: Python module path to module
    :type blueprint: str
    """

    try:
        __import__('{0}.models'.format(blueprint))
    except ImportError:
        # TODO: Log this at debug level
        pass


def load_blueprint(app, blueprint):
    """
    Load the blueprint and register the routes

    :param app: Flask application instance
    :type app: flask.app.Flask

    :param blueprint: Python module path to module
    :type blueprint: str
    """

    try:
        module = __import__(
            '{0}.routes'.format(blueprint),
            fromlist=['pravis'])
    except ImportError:
        raise ImproperlyConfigured(
            'routes.py not defined for {0} blueprint.'.format(blueprint))

    try:
        for route, view in module.routes:
            module.blueprint.add_url_rule(route, view_func=view)
    except AttributeError:
        raise ImproperlyConfigured('routes list is not defined')

    app.register_blueprint(module.blueprint)


def register_extenstions(app):
    """
    Register Flask extenstions with application context

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

    # Admin
    admin.init_app(app)


def register_blueprints(app):
    """
    Load application blueprints from config, similar to Django INSTALLED_APPS
    setting which is literally a list of strings of python module paths.

    Each blueprint can contain the following files:

        - __init__.py - Instantiates the blueprint
        - admin.py - routes for registering admin views
        - models.py - SQL Alchemy models
        - routes.py - Instantiates the blueprint and contains a list named
                      routes contain tuples of (url, view_func)

    :param app: Flask application instance
    :type app: flask.app.Flask
    """

    for blueprint in app.config.get('BLUEPRINTS', []):
        load_models(blueprint)
        load_blueprint(app, blueprint)


def register_uploads(app):
    """
    Register upload endpoints to be served by werkzeug in development,
    do not use for production.

    :param app: Flask application instance
    :type app: flask.app.Flask
    """

    app.add_url_rule('/uploads/<filename>', 'uploads', build_only=True)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/uploads':  app.config['UPLOAD_DIR']
    })
