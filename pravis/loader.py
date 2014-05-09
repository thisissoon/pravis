# -*- coding: utf-8 -*-

"""
.. module:: pravis.app.loader
    :synopsis: Helper utilities for application factory, mostly utilities
               around auto loading blueprints, models and admin registration.
"""

import os

from flask.ext.security import SQLAlchemyUserDatastore
from pravis.ext import db, migrate, security, xmlrpc, velox, via
from werkzeug import SharedDataMiddleware


admin = None


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
    from pravis.auth.models import User, Role
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore)

    # XMLRPC
    from pravis.simple.xmlrpc import search
    xmlrpc.connect(app, '/simple/')
    xmlrpc.register(search, 'search')

    # Admin
    from flask.ext.admin import Admin
    from pravis.views.admin import AdminHomeView

    global admin

    admin = Admin(
        name='Pravis',
        index_view=AdminHomeView(name='Dashboard'),
        base_template='layout/admin.html')
    admin.init_app(app)

    # Velox
    velox.init_app(app)

    # Via
    via.init_app(app, flask_admin=admin)


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
