# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
.. module:: manage
   :synopsis: Flask manager for perfomining management commands such as
              running a local development server.
"""

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell, Server
from flypi.app import create_app
from flypi.ext import db
from flypi.auth.models import User


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    """
    Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """

    return {
        'app': app,
        'db': db,
        'User': User
    }


@manager.command
def schema_diagram():
    """
    Draw an Entity Relationship Diagram
    """

    from sqlalchemy_schemadisplay import create_schema_graph

    graph = create_schema_graph(
        metadata=db.MetaData(app.config['SQLALCHEMY_DATABASE_URI']),
        show_datatypes=True,
        show_indexes=True
    )

    graph.write_png('schema.png')


manager.add_command("server", Server())
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=_make_context))


if __name__ == "__main__":
    manager.run()
