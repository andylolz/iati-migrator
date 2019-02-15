"""The app module, containing the app factory function."""
from flask import Flask, render_template

from . import public
from .extensions import cache, csrf_protect, debug_toolbar


def create_app(config_object='iati_migrator.settings'):
    """Application factory.

    As explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    cache.init_app(app)
    csrf_protect.init_app(app)
    debug_toolbar.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
