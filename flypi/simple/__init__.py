# -*- coding: utf-8 -*-

"""
.. module:: flypi.simple
   :synopsis: Blueprint setup for Simple module
"""

from flask.blueprints import Blueprint
from flypi.simple.views import LoginView

blueprint = Blueprint('simple', __name__, url_prefix='/simple/')
blueprint.add_url_rule('/', view_func=LoginView.as_view('simple'))
