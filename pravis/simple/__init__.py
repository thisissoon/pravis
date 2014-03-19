# -*- coding: utf-8 -*-

"""
.. module:: pravis.simple
   :synopsis: Blueprint setup for Simple module
"""

from flask.blueprints import Blueprint
from pravis.simple.views import SimpleUploadView, SimpleListView

blueprint = Blueprint('simple', __name__, url_prefix='/simple/')

#
# Routes
#

blueprint.add_url_rule(
    '/',
    view_func=SimpleUploadView.as_view('simple_upload'),
    methods=['POST'])
blueprint.add_url_rule(
    '/',
    view_func=SimpleListView.as_view('simple_list'),
    methods=['GET'])
