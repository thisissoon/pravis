# -*- coding: utf-8 -*-

"""
.. module:: pravis.models
   :synopsis: Base models all models should inherit from
"""

import datetime

from pravis.ext import db


class BaseModel(db.Model):

    # This is an abstract model, i.e no Table
    __abstract__ = True

    # Timestamps
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
