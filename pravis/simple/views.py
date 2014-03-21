# -*- coding: utf-8 -*-

"""
.. module:: pravis.simple.views
   :synopsis: Simple module views.
"""

from flask import request
from flask.ext.login import current_user
from flask.views import MethodView
from pravis.auth.decorators import basic_auth
from pravis.ext import db
from pravis.package.models import Package, Release
from pravis.simple.forms import ReleaseForm
from werkzeug.exceptions import BadRequest, Forbidden


class SimpleListView(MethodView):

    def get(self):
        return 'List of packages'


class SimpleUploadView(MethodView):

    decorators = [basic_auth, ]

    def post(self):
        name = request.values.get('name')
        version = request.values.get('version')

        if not name or not version:
            raise BadRequest('Missing package name or version')

        package = db.session.query(Package).filter_by(name=name).first()

        if package:

            # Packages mirrored from the official pypi cannot be overritten
            if package.mirrored:
                raise BadRequest('Package is a PyPi mirrored package, cannot'
                                 'overwrite package.')

            # If current logging in user is not an own of the package forbid
            # their access
            if not current_user in package.owners:
                raise Forbidden('You are not an owner of this package and'
                                'cannot update this package.')

        # If package does not exist create it with current user as the owner
        if not package:
            package = Package(name=name, mirrored=False)
            package.owners.append(current_user)
            db.session.add(package)
            db.session.commit()

        form = ReleaseForm(request.values, csrf_enabled=False)

        if not form.validate():
            raise BadRequest('Bad release data recived')

        release = Release(**form.data)
        release.package = package.id
        release.user = current_user.id
        db.session.add(release)
        db.session.commit()

        classifiers = request.values.getlist('classifiers')

        return 'SUCCESS'
