# -*- coding: utf-8 -*-

"""
.. module:: pravis.simple.views
   :synopsis: Simple module views.
"""

import os

from flask import current_app, request
from flask.ext.login import current_user
from flask.views import MethodView
from pravis.auth.decorators import basic_auth
from pravis.ext import db
from pravis.package.models import Classifier, File, Package, Release
from pravis.simple.forms import ReleaseForm
from werkzeug.exceptions import BadRequest, Forbidden
from werkzeug.utils import secure_filename

from flask.ext.velox.views.sqla import read


class SimpleListView(read.ModelListView):
    """ Renders a simpoe list of packages used by installers to search for
    packages by name.

    **HTTP Methods:**
    * ``GET``
    """

    model = Package
    template = 'list.html'
    objects_context_name = 'packages'
    paginate = False


class SimpleDetailView(read.ObjectView):
    """ Package detail view rendering package download links.

    **HTTP Methods:**
    * ``GET``
    """

    model = Package
    template = 'detail.html'
    object_context_name = 'package'

    def get_object(self):
        name = self.name  # name not optional
        query = Package.query.filter_by(name=name)
        # Version is optional
        try:
            version = self.version
        except AttributeError:
            version = None
        else:
            query = query.filter(Release.version == version)
        obj = query.first_or_404()
        return obj


class SimpleUploadView(MethodView):

    methods = ['POST', ]
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

        # Ensure the request contains a file
        if not 'content' in request.files:
            raise BadRequest('Missing file')

    def create_release(self, form):
        """
        Create a release object for the package from the release form
        data if valid

        :param form: Release form with data
        :type form: pravis.simple.forms.ReleaseForm

        :returns: pravis.package.models.Release -- Release object
        """

        release = Release(**form.data)
        release.package_id = self.package.id
        release.user_id = current_user.id

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

    def add_file(self, release):
        """
        Save the file locally, this is to be replaced with a way of defining
        different storage backends.

        :param release: The packages release object
        :type release: pravis.package.models.Release
        """

        f = request.files.get('content')
        filename = secure_filename(f.filename)
        path = os.path.join(
            current_app.config['UPLOAD_PACKAGE_DIR'],
            filename)
        f.save(path)

        release_file = File(
            release_id=release.id,
            size=os.stat(path).st_size,
            filename=filename,
            filetype=request.values.get('filetype'),
            storage=path)

        db.session.add(release_file)
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
        self.add_file(release)
        self.add_classifiers(release)

        return 'SUCCESS'
