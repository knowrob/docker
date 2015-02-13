#
# Based on https://github.com/lingthio/Flask-User-starter-app
# 
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


import logging
from logging.handlers import SMTPHandler
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask.ext.babel import Babel

from webrob.startup.init_db import *



def init_app(app, db, extra_config_settings={}):

    # Initialize app config settings
    app.config.from_object('webrob.config.settings')        # Read config from 'app/settings.py' file
    app.config.update(extra_config_settings)                # Overwrite with 'extra_config_settings' parameter
    if app.testing:
        app.config['WTF_CSRF_ENABLED'] = False              # Disable CSRF checks while testing

    # Setup Flask-Mail
    mail = Mail(app)

    babel = Babel(app)

    # Setup Flask-User to handle user account related forms
    from webrob.models.users import User
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # Load all models.py files to register db.Models with SQLAlchemy
    from webrob.models import users
    from webrob.models import tutorials

    # Load all views.py files to register @app.routes() with Flask
    from webrob.pages import views
    from webrob.pages import editor
    from webrob.pages import log
    from webrob.pages import login
    from webrob.pages import api

    init_db(app, db)

    return app

