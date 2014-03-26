# -*- coding: utf-8 -*-

"""
.. module:: pravis.package.routes
   :synopsis: Flask blueprint instantiation and route definitions
"""

from flask.blueprints import Blueprint


blueprint = Blueprint(
    'package',
    __name__,
    url_prefix='/package',
    template_folder='templates')

routes = []
