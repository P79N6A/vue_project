"""Admin module initialization.

create_app() needs to be called from someplace for the module to run.

"""
import logging
from logging.handlers import SMTPHandler

from flask import Flask, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_session import Session

db = SQLAlchemy()
sess = Session()


def create_app(extra_config_settings={}):
    """Create the Flask app.

    Attaches all modules.
    Creates authentication handlers.
    Loads blueprints.

    """
    app = Flask(__name__)

    # Load settings.
    app.config.from_object("app.settings")
    app.config.update(extra_config_settings)
    app.url_map.strict_slashes = False

    # Setup and initialize modules.
    db.init_app(app)
    sess.init_app(app)
    app.session_interface.db.create_all()

    # Handle auth.
    from app.models import Employee
    from flask_login import LoginManager, user_logged_in, user_logged_out
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "/login/"

    @user_logged_in.connect_via(app)
    def login_user(*args, **kwargs):
        """Add user to session."""
        session["email"] = flask_login.current_user.email

    @user_logged_out.connect_via(app)
    def logout_user(*args, **kwargs):
        """Remove data from session.

        Removing "_csrf_token" and "_permanent" can in some situations
        make the client and server disagree about auth status, resulting
        in the user unable to access any pages until a cache clear or server
        restart. So those are left in.

        """
        to_pop = []
        for i in session:
            if (i not in ["_csrf_token", "_permanent", "id_tracking"]):
                to_pop.append(i)
        for i in to_pop:
            session.pop(i)

    @login_manager.user_loader
    def load_user(_id):
        """Set employee as the user model to log in."""
        return db.session.query(Employee).get(int(_id))

    @login_manager.unauthorized_handler
    def unauthorized_user():
        """Take unauthorized users to /login/."""
        return redirect("/login/")

    # Register blueprints.
    from app.controllers.misc import misc_blueprint
    from app.controllers.queries import query_blueprint
    from app.controllers.edits import edit_blueprint

    app.register_blueprint(misc_blueprint)
    app.register_blueprint(query_blueprint)
    app.register_blueprint(edit_blueprint)

    @app.errorhandler(404)
    def page_not_found(error):
        """All routes not defined can reroute to the index for this app."""
        return redirect(url_for("misc.index"))

    @app.teardown_request
    def teardown_request(exception):
        """Rollback db errors."""
        if exception:
            db.session.rollback()
        db.session.remove()

    from .SessionTablesMixin import SessionTablesMixin
    SessionTablesMixin(app)

    # Handle error logging
    if not app.debug:
        auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr='admin-site@' + app.config["MAIL_SERVER"],
            toaddrs=app.config["ADMINS"],
            subject="Admin Site Error",
            credentials=auth,
            secure=None
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    return app
