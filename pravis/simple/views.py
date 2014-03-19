# -*- coding: utf-8 -*-

"""
.. module:: pravis.simple.views
   :synopsis: Simple module views.
"""

from flask.ext.login import current_user
from flask.views import MethodView
from pravis.auth.decorators import basic_auth


class SimpleListView(MethodView):

    def get(self):
        return 'List of packages'


class SimpleUploadView(MethodView):

    decorators = [basic_auth]

    def post(self):
        return 'uploading packages'
