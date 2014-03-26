# -*- coding: utf-8 -*-

"""
.. module:: pravis.views.admin
   :synopsis: Base admin views
"""

from flask.ext import admin
from flask.ext.login import current_user


class BaseAdminView(admin.BaseView):

    def is_accessible(self):
        return current_user.is_authenticated()
