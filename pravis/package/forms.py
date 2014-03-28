# -*- coding: utf-8 -*-

"""
.. module:: pravis.packages.forms
   :synopsis: WTForms for packages models
"""

from flask.ext.wtf import Form
from pravis.ext import db
from pravis.package.models import Package
from wtforms_alchemy import model_form_factory

ModelForm = model_form_factory(Form)


class PackageForm(ModelForm):

    class Meta:
        model = Package

    @classmethod
    def get_session():
        return db.session
