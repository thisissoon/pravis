# -*- coding: utf-8 -*-

"""
.. module:: pravis.auth.util
   :synopsis: Authentication helper utility methods
"""


def basic_auth_identity(auth):
    """
    Take the raw header and split it returning the identity hash

    :param auth: The HTTP_AUTHORIZATION header
    :type auth: str

    :returns: str or None -- The identity
    """

    try:
        method, identity = auth.split(' ')
    except (ValueError, TypeError):
        return None

    if method and method.lower() == 'basic':
        return identity


def basic_auth_credentials(identity):
    """
    For the hashed basic auth identity decode it and return the
    usernamd and password provided

    :param identity: The hashed basic auth identity
    :type identity: str

    :returns: tuple -- Username, Password
    """

    credentials = identity.strip().decode('base64')

    try:
        username, password = credentials.split(':', 1)
    except (ValueError, TypeError):
        return None, None

    return username, password


def basic_auth_decode(auth):
    """
    Decode the HTTP_AUTHORIZATION header returning a tuple of the
    usernamd and password

    :param auth: The value of HTTP_AUTHORIZATION header
    :type auth: str

    :returns: tuple -- Username, Password
    """

    username = None
    password = None

    if auth:
        identity = basic_auth_identity(auth)
        username, password = basic_auth_credentials(identity)

    return username, password
