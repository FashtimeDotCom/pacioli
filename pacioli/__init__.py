from flask import Flask
from flask.ext.security import Security
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask_admin import helpers as admin_helpers

from pacioli import assets
from pacioli.models import db, User, Role, user_datastore, register_models
from pacioli.extensions import cache, assets_env, debug_toolbar, admin, mail


def create_app(object_name, env="prod"):
    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env
    db.init_app(app)
    mail.init_app(app)
    security = Security(app, user_datastore)

    @security.context_processor
    def security_context_processor():
        return dict(admin_base_template=admin.base_template,
                    admin_view=admin.index_view,
                    h=admin_helpers)

    admin.init_app(app)

    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    with app.app_context():
        register_models()

    import pacioli.views.admin_views
    import pacioli.views.bookkeeping_views
    import pacioli.views.accounting_views
    import pacioli.views.ofx_views
    import pacioli.views.amazon_views
    import pacioli.views.payroll_views

    return app
