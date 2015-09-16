#
# Based on https://github.com/lingthio/Flask-User-starter-app
# 
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from logging.handlers import SMTPHandler
import os
import datetime

from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask.ext.babel import Babel

from webrob.utility import random_string
from webrob.startup.init_db import *
from webrob.startup.init_webapp import *
from webrob.models.users import Role, User

from werkzeug.security import generate_password_hash

def add_user(db,user_manager,name,mail,pw,roles):
    if pw==None or len(pw)<4: return
    if User.query.filter(User.username==name).first(): return
    user = User(username=name, email=mail, active=True, password=user_manager.hash_password(pw), confirmed_at=datetime.datetime.utcnow())
    for r in roles:
        x = Role.query.filter(Role.name==r).first()
        if x==None:
            app.logger.info("Unable to find role: " + str(r))
        else:
            user.roles.append(x)
    db.session.add(user)
    db.session.commit()

def init_app(app, db_instance, extra_config_settings={}):
    # Initialize app config settings
    app.config.from_object('webrob.config.settings')        # Read config from 'app/settings.py' file
    app.config.update(extra_config_settings)                # Overwrite with 'extra_config_settings' parameter
    if app.testing:
        app.config['WTF_CSRF_ENABLED'] = False              # Disable CSRF checks while testing
    if os.environ['EASE_DEBUG'] == 'true':
        app.config['DEBUG'] = True
        app.config['SECRET_KEY'] = app.config['DEV_SECRET_KEY']
    else:
        try:
            app.config['SECRET_KEY'] = open('/etc/ease_secret/secret', 'rb').read()
        except IOError:
            app.config['SECRET_KEY'] = random_string(64)

    # Setup Flask-Mail
    mail = Mail(app)

    babel = Babel(app)

    # Setup Flask-User to handle user account related forms
    from webrob.models.users import User
    db_adapter = SQLAlchemyAdapter(db_instance, User)
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # Load all models.py files to register db.Models with SQLAlchemy
    from webrob.models import users
    from webrob.models import tutorials
    from webrob.models import experiments

    # Load all views.py files to register @app.routes() with Flask
    from webrob.pages import api
    from webrob.pages import db
    from webrob.pages import editor
    from webrob.pages import experiments
    from webrob.pages import knowrob
    from webrob.pages import login
    from webrob.pages import meshes
    from webrob.pages import mongo
    from webrob.pages import tutorials
    
    init_db(app, db_instance)
    init_webapp(app, db_instance)
    
    add_user(app,db_instance,user_manager,'admin', 'openease.iai@gmail.com',
             os.environ.get('OPENEASE_ADMIN_PASSWORD'), ['admin'])

    app.logger.info("Webapp started.")
    return app
