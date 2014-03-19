# -*- coding: utf-8 -*-

"""
.. module:: pravis.auth.decorators
   :synopsis: Decorators to assist with authentication
"""

from flask import abort, request
from flask.ext.login import login_user
from flask.ext.security.utils import verify_and_update_password
from pravis.ext import db
from pravis.auth.models import User
from pravis.auth.util import basic_auth_decode


def basic_auth(func):
    """
    Authenticate user from Basic Auth which is the autentication
    method for uploading packages
    """

    def decorator(*args, **kwargs):

        username, password = basic_auth_decode(
            request.headers.get('AUTHORIZATION'))

        if not username or not password:
            abort(401)

        user = db.session.query(User).filter_by(email=username).first()
        if not user:
            abort(401)

        if not verify_and_update_password(password, user):
            abort(401)

        login_user(user)

        return func(*args, **kwargs)
    return decorator
