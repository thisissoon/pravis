from flask.ext.via.routers import Include
from flask.ext.via.routers.default import Blueprint

routes = [
    # Authentication Blueprint
    Blueprint(
        'auth',
        'pravis.auth',
        url_prefix='/auth',
        template_folder='templates'),
    # Simple Index Blueprint
    Blueprint(
        'simple',
        'pravis.simple',
        url_prefix='/simple',
        template_folder='templates'),
    # Package Routes
    Include('pravis.package.routes', url_prefix='/package')
]
