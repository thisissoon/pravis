# -*- coding: utf-8 -*-

"""
.. module:: pravis.simple.routes
   :synopsis: Flask blueprint instantiation and route definitions
"""

from flask.blueprints import Blueprint
from pravis.simple.views import (
    SimpleListView,
    SimpleDetailView,
    SimpleUploadView)

blueprint = Blueprint(
    'simple',
    __name__,
    url_prefix='/simple',
    template_folder='templates')

#
# Routes
#

routes = [
    ('/', SimpleListView.as_view('list')),
    ('/', SimpleUploadView.as_view('upload')),
    ('/<name>/', SimpleDetailView.as_view('detail')),
    ('/<name>/<version>', SimpleDetailView.as_view('detail-version')),
]
