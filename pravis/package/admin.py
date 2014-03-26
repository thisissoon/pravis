# -*- coding: utf-8 -*-

"""
.. module:: pravis.package.admin
   :synopsis: Flask super admin integration for package blueprint
"""

from flask.ext import admin
from flask.views import MethodView
from pravis.views.admin import BaseAdminView


class PackageListView(BaseAdminView):

    @admin.expose_plugview('/')
    class index(MethodView):

        def get(self, admin):
            return admin.render('admin/list.html')
