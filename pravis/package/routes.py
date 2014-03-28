# -*- coding: utf-8 -*-

"""
.. module:: pravis.package.routes
   :synopsis: Flask blueprint instantiation and route definitions
"""

from flask.blueprints import Blueprint
from pravis.package.admin import PackageAdminView


blueprint = Blueprint(
    'package',
    __name__,
    url_prefix='/package',
    template_folder='templates')

# Public routes
routes = []

# Admin Views (Flask-Admin)
admin = [
    PackageAdminView(
        name='Packages',
        url='packages',
        endpoint='admin.packages')
]
