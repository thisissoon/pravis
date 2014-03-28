# -*- coding: utf-8 -*-

"""
.. module:: pravis.package.admin
   :synopsis: Flask super admin integration for package blueprint
"""

from flask.ext import admin
from flask.views import MethodView
from pravis.package.models import Package
from pravis.views.admin import BaseAdminView


class PackageListView(BaseAdminView):

    @admin.expose_plugview('/')
    @admin.expose_plugview('/<int:page>/')
    class index(MethodView):

        def get(self, admin, page=1):
            pages = Package.query.join().paginate(page, 31, False)
            return admin.render('admin/list.html', **{
                'pages': pages
            })
