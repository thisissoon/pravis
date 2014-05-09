# -*- coding: utf-8 -*-

"""
.. module:: pravis.package.routes
   :synopsis: Flask blueprint instantiation and route definitions
"""

from flask.ext.via.routers.admin import AdminRoute
from pravis.package.admin import PackageAdminView

#
# Routes
#

routes = [
    AdminRoute(PackageAdminView(
        name='Packages',
        url='packages',
        endpoint='admin.packages'))
]
