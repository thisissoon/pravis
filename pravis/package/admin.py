# -*- coding: utf-8 -*-

"""
.. module:: pravis.package.admin
   :synopsis: Flask super admin integration for package blueprint
"""

from flask import request, flash
from flask.ext import admin
from flask.views import MethodView
from pravis.ext import db
from pravis.package.forms import PackageForm
from pravis.package.models import Package
from pravis.views.admin import BaseAdminView


class PackageAdminView(BaseAdminView):

    @admin.expose_plugview('/')
    @admin.expose_plugview('/<int:page>')
    class index(MethodView):

        def get(self, admin, page=1):
            pages = Package.query.paginate(page, 31, False)
            return admin.render('admin/list.html', **{
                'pages': pages
            })

    @admin.expose_plugview('/edit/<int:id>')
    class edit(MethodView):

        def get(self, admin, id):
            package = Package.query.filter_by(id=id).first_or_404()
            form = PackageForm(obj=package)
            return admin.render('admin/edit.html', **{
                'form': form,
                'package': package
            })

        def post(self, admin, id):
            package = Package.query.filter_by(id=id).first_or_404()
            form = PackageForm(request.values, obj=package)
            if form.validate():
                Package.query.filter_by(id=id).update(form.data)
                db.session.commit()
                flash(u'Package ({0}) updated'.format(package.name), 'success')
            return admin.render('admin/edit.html', **{
                'form': form,
                'package': package
            })
