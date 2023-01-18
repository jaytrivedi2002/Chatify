from flask import Flask
from .views import view
from .filters import _slice


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Extend Application
        app.register_blueprint(view, url_prefix="/")
        # Context processor for the slice to be returned in definition
        @app.context_processor
        def slice():
            return dict(slice=_slice)
        return app
