# -*- coding: utf-8 -*-

"""
.. module:: pravis.db.mixins
   :synopsis: Helper mixins to extend default model functionality
"""

import datetime

from pravis.ext import db


class CreateUpdateMixin(object):

    # Timestamps
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
