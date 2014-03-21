# -*- coding: utf-8 -*-

"""
.. module:: pravis.simple.forms
   :synopsis: WTForms for simple api data validation
"""

from flask.ext.wtf import Form
from pravis.package.models import Release
from wtforms_alchemy import model_form_factory


ModelForm = model_form_factory(Form)


class ReleaseForm(ModelForm):

    class Meta:
        model = Release
