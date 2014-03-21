# -*- coding: utf-8 -*-

"""
.. module:: pravis.auth.decorators
   :synopsis: Decorators to assist with authentication
"""

from flask import request
from flask.ext.login import login_user
from flask.ext.security.utils import verify_and_update_password
from pravis.ext import db
from pravis.auth.models import User
from pravis.auth.util import basic_auth_decode
from werkzeug.exceptions import Unauthorized


def basic_auth(func):
    """
    Authenticate user from Basic Auth which is the autentication
    method for uploading packages
    """

    def decorator(*args, **kwargs):

        username, password = basic_auth_decode(
            request.headers.get('AUTHORIZATION'))

        if not username or not password:
            raise Unauthorized('Username or Password not supplied')

        user = db.session.query(User).filter_by(email=username).first()
        if not user:
            raise Unauthorized('User does not exist, please register')

        if not verify_and_update_password(password, user):
            raise Unauthorized('Incorrect username or password')

        login_user(user)

        return func(*args, **kwargs)
    return decorator
