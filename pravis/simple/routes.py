# -*- coding: utf-8 -*-

"""
"""

from flask.ext.via.routers.default import Pluggable
from pravis.simple.views import (
    SimpleListView,
    SimpleDetailView,
    SimpleUploadView)


#
# Routes
#

routes = [
    Pluggable('/', view_func=SimpleListView.as_view('list')),
    Pluggable('/', view_func=SimpleUploadView.as_view('upload')),
    Pluggable('/<name>/', view_func=SimpleDetailView.as_view('detail')),
    Pluggable(
        '/<name>/<version>',
        view_func=SimpleDetailView.as_view('detail-version')),
]
