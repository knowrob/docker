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

from webrob.pages.utility import random_string
from webrob.startup.init_db import *
from webrob.pages.routes import register_routes
from webrob.models.users import Role

from werkzeug.security import generate_password_hash

def get_role_by_name(db_adapter, role_name):
    roles = db_adapter.find_all_objects(Role)
    for r in roles:
        if str(r.name) == role_name: return r
    return None

def init_admin_user(app, user_manager):
    db_adapter = user_manager.db_adapter
    users = db_adapter.find_all_objects(db_adapter.UserClass)
    user_names = map(lambda r: r.username, users)
    
    if "admin" in user_names: return
    app.logger.info("Creating 'admin' user...")
        
    # Find next id
    new_user_id = 1
    if len(user_names)>0:
        new_user_id = max(map(lambda r: r.id, users))+1
    
    user_fields = {}
    user_auth_fields = {}
    
    user_fields['id'] = new_user_id
    user_fields['username'] = 'admin'
    user_fields['email'] = 'openease.iai@gmail.com'
    
    # Enable user account
    if db_adapter.UserProfileClass:
        if hasattr(db_adapter.UserProfileClass, 'active'):
            user_auth_fields['active'] = True
        elif hasattr(db_adapter.UserProfileClass, 'is_enabled'):
            user_auth_fields['is_enabled'] = True
        else:
            user_auth_fields['is_active'] = True
    else:
        if hasattr(db_adapter.UserClass, 'active'):
            user_fields['active'] = True
        elif hasattr(db_adapter.UserClass, 'is_enabled'):
            user_fields['is_enabled'] = True
        else:
            user_fields['is_active'] = True
    
    hashed_password = user_manager.hash_password(os.environ.get('OPENEASE_MAIL_PASSWORD'))
    if db_adapter.UserAuthClass:
        user_auth_fields['password'] = hashed_password
    else:
        user_fields['password'] = hashed_password
    
    user = db_adapter.add_object(User, **user_fields)
    user.roles.append(get_role_by_name(db_adapter, "ADMIN"))
    db_adapter.update_object(user, confirmed_at=datetime.datetime.utcnow())
    
    if db_adapter.UserAuthClass:
        user_auth = db_adapter.add_object(db_adapter.UserAuthClass, **user_auth_fields)


def init_user_roles(user_manager):
    db_adapter = user_manager.db_adapter
    roles = db_adapter.find_all_objects(Role)
    role_names = map(lambda r: r.name, roles)
    init_role_names = [ "ADMIN", "USER", "EDITOR", "REVIEWER" ]
        
    # Find next id
    new_role_id = 1
    if len(role_names)>0:
        new_role_id = max(map(lambda r: r.id, roles))+1
        
    for role_name in init_role_names:
        if not role_name in role_names:
            db_adapter.add_object(Role, id=new_role_id, name=role_name)
            new_role_id += 1


def init_app(app, db, extra_config_settings={}):

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
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)     # Init Flask-User and bind to app

    # Load all models.py files to register db.Models with SQLAlchemy
    from webrob.models import users
    from webrob.models import tutorials

    # Load all views.py files to register @app.routes() with Flask
    register_routes()

    init_db(app, db)
    
    # Initialize DB content
    init_user_roles(user_manager)
    init_admin_user(app, user_manager)
    db_adapter.commit()

    app.logger.info("Webapp started.")
    return app

