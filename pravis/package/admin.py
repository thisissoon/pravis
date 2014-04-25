# -*- coding: utf-8 -*-

"""
.. module:: pravis.package.admin
   :synopsis: Flask super admin integration for package blueprint
"""

from flask.ext import admin
from flask.ext.login import current_user
from flask.ext.velox.formatters import bool_admin_formatter
from flask.ext.velox.admin.views.sqla.read import AdminModelTableView
from flask.ext.velox.admin.views.sqla.forms import (
    AdminCreateModelView,
    AdminUpdateModelView)
from flask.ext.velox.admin.views.sqla.delete import (
    AdminDeleteObjectView)
from pravis.ext import db
from pravis.package.forms import PackageForm
from pravis.package.models import Package


class PackageAdminView(admin.BaseView):

    def is_accessible(self):
        if current_user.is_authenticated():
            return True
        return False

    @admin.expose_plugview('/')
    class index(AdminModelTableView):
        model = Package
        columns = ['name', 'mirrored', 'latest_version']
        formatters = {
            'mirrored': bool_admin_formatter
        }

    @admin.expose_plugview('/create')
    class create(AdminCreateModelView):
        model = Package
        form = PackageForm
        session = db.session

    @admin.expose_plugview('/update/<int:id>')
    class update(AdminUpdateModelView):
        model = Package
        form = PackageForm
        session = db.session

    @admin.expose_plugview('/delete/<int:id>')
    class delete(AdminDeleteObjectView):
        model = Package
        session = db.session
