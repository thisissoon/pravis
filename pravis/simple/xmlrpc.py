# -*- coding: utf-8 -*-

"""
.. module:: pravis.simple.xmlrpc
   :synopsis: Simple views for handling xmlrpc requests such as pip search
"""

from pravis.ext import db
from pravis.package.models import Package, Release
from sqlalchemy import or_, and_


def search(query, operator, *kwargs):
    """
    Query the local database for packages matching the given query
    from pip search.

    :param query: The search query
    :type query: dict

    :param operator: The operator to use when querying the db, eg AND / OR
    :type operator: str

    :returns: list -- a list of packages matching the query if any
    """

    results = []
    names = query.get('name')
    operator_ = {
        'and': and_,
        'or': or_
    }.get(operator, or_)

    terms = [Package.name.ilike(u'{0}'.format(name)) for name in names]
    clauses = operator_(*terms)
    query = db.session.query(Package).filter(clauses)

    packages = query.all()

    for package in packages:
        release = db.session.query(Release)\
            .filter_by(package=package)\
            .order_by(Release.created.desc())\
            .first()

        results.append({
            'name': package.name,
            'summary': release.summary,
            'version': release.version,
            '_pypi_ordering': 0,
        })

    return results
