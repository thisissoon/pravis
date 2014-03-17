# -*- coding: utf-8 -*-

"""
.. module:: pravis.simple.views
   :synopsis: Simple module views.
"""

from flask.views import MethodView


class SimpleView(MethodView):

    def get():
        return 'listing packages'

    def post(self):
        return 'uploading packages'
