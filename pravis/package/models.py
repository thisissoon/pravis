# -*- coding: utf-8 -*-

"""
.. module:: pravis.package.models
    :synopsis: Models for uploading python packages to the index
"""

from pravis.ext import db
from pravis.models import CreateUpdateMixin


class Package(db.Model, CreateUpdateMixin):

    __tablename__ = 'package'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Package attributes
    name = db.Column(db.Unicode(length=128), unique=True)
    mirrored = db.Column(db.Boolean, default=True)

    # Owners of the package
    owners = db.relationship(
        'User',
        secondary='package_owners',
        backref=db.backref('packages', lazy='dynamic'))


class PackageOwners(db.Model, CreateUpdateMixin):

    __tablename__ = 'package_owners'

    # Foreign Keys
    package_id = db.Column(
        db.Integer,
        db.ForeignKey('package.id'),
        primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True)


class Classifier(db.Model, CreateUpdateMixin):

    __tablename__ = 'classifier'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Classifier attributes
    name = db.Column(db.Unicode(length=128))


class Release(db.Model, CreateUpdateMixin):
    """
    Package release data, the fields here more or less map to attributes
    in setup.py, for example field author = author keyword argument in
    setup(), there are the following exceptions however:

        home_page = url
        summary = description
        description = long_description
    """

    __tablename__ = 'release'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Release attributes - comes from setup.py
    author = db.Column(db.Unicode(128), nullable=True)
    author_email = db.Column(db.Unicode(256), nullable=True)
    home_page = db.Column(db.Unicode(512), nullable=True)
    download_url = db.Column(db.Unicode(512), nullable=True)
    summary = db.Column(db.UnicodeText, nullable=True)  # description
    description = db.Column(db.UnicodeText, nullable=True)
    license = db.Column(db.UnicodeText, nullable=True)
    metadata_version = db.Column(
        db.Unicode(512),
        default='1.0',
        nullable=True)
    version = db.Column(
        db.Unicode(512),
        default='1.0',
        nullable=True)

    # Relations
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    package = db.Column(db.Integer, db.ForeignKey('package.id'))
    classifiers = db.relationship(
        'Classifier',
        secondary='release_classifiers',
        backref=db.backref('releases', lazy='dynamic')
    )


class ReleaseClassifiers(db.Model, CreateUpdateMixin):

    __tablename__ = 'release_classifiers'

    # Foreign Keys
    release_id = db.Column(
        db.Integer,
        db.ForeignKey('release.id'),
        primary_key=True)
    classifier_id = db.Column(
        db.Integer,
        db.ForeignKey('classifier.id'),
        primary_key=True)


class File(db.Model, CreateUpdateMixin):

    __tablename__ = 'file'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # File attributes
    size = db.Column(db.Integer, nullable=True)
    filetype = db.Column(db.Unicode(length=32))
    filename = db.Column(db.Unicode(length=32))
    storage = db.Column(db.Unicode(length=512))

    # Relations
    release = db.Column(db.Integer, db.ForeignKey('release.id'))
