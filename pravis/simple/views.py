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
from pravis.package.models import Classifier, Package, Release
from pravis.simple.forms import ReleaseForm
from werkzeug.exceptions import BadRequest, Forbidden


class SimpleListView(MethodView):

    def get(self):
        return 'List of packages'


class SimpleUploadView(MethodView):

    decorators = [basic_auth, ]

    def authorise_upload(self):
        """
        Method checks if the user can upload this package if it already exists.
        """

        # Packages mirrored from the official pypi cannot be overritten
        if self.package.mirrored:
            raise BadRequest('Package is a PyPi mirrored package, cannot'
                             'overwrite package.')

        # If current logging in user is not an own of the package forbid
        # their access
        if not current_user in self.package.owners:
            raise Forbidden('You are not an owner of this package and'
                            'cannot update this package.')

    def create_release(self, form):
        """
        Create a release object for the package from the release form
        data if valid

        :param form: Release form with data
        :type form: pravis.simple.forms.ReleaseForm

        :returns: pravis.package.models.Release -- Release object
        """

        release = Release(**form.data)
        release.package = self.package.id
        release.user = current_user.id

        db.session.add(release)
        db.session.commit()

        return release

    def add_classifiers(self, release):
        """
        Add the release classifers set in the packages setup.py

        :param release: The packages release object
        :type release: pravis.package.models.Release
        """

        classifiers = [{'name': v} for v in
                       request.values.getlist('classifiers')]

        objects = Classifier.get_or_create_from_list(
            classifiers)

        for exists, classifier in objects:
            classifier.releases.append(release)
            db.session.commit()

    def post(self):
        """
        Process post request to simple endpoint. This endpoint allows for
        packages to be uploade provided the following requirements are met:

            - User exists
            - User is an owner of the package
            - Package is not mirrored from PyPi

        :returns: str -- HTTP response body
        """

        exists, self.package = Package.get_or_create(
            commit=False,
            name=request.values.get('name'))

        if exists:
            self.authorise_upload()

        if not exists:
            self.package.owners.append(current_user)
            db.session.add(self.package)
            db.session.commit()

        form = ReleaseForm(request.values, csrf_enabled=False)

        if not form.validate():
            raise BadRequest('Bad release data recived')

        release = self.create_release(form)
        self.add_classifiers(release)

        return 'SUCCESS'
