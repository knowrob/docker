from flask import request, render_template, jsonify
from flask_user import current_user
from flask_user import current_app
from flask_user import login_required

import json

from webrob.app_and_db import app
from webrob.utility import admin_required
from webrob.models.users import Role

__author__ = 'danielb@cs.uni-bremen.de'

@app.route('/admin/users')
@admin_required
def admin_users():
    return render_template('admin_users.html', **locals())

@app.route('/admin/user_list', methods=['POST'])
@admin_required
def admin_user_list():
    db_adapter = current_app.user_manager.db_adapter
    users = db_adapter.find_all_objects(db_adapter.UserClass)
    user_list = map(lambda u: {
        'id': str(u.id),
        'username': str(u.username),
        'email': str(u.email),
        'role': str(u.first_role())
    }, users)
    return jsonify(users=user_list)

def get_role_by_name(role_name):
    db_adapter = current_app.user_manager.db_adapter
    roles = db_adapter.find_all_objects(Role)
    for r in roles:
        if str(r.name) == role_name: return r
    return None

@app.route('/admin/user_save', methods=['POST'])
@admin_required
def admin_user_save():
    db_adapter = current_app.user_manager.db_adapter
    user_update = json.loads(request.data)
    user_db = db_adapter.get_object(db_adapter.UserClass, user_update['id'])
    
    app.logger.info("Updating user: " + str(user_db.username) + "[" + str(user_db.id) + "]."  + "\n")
    # Set role
    role = get_role_by_name(user_update['role'])
    if role!=None:
        for r in user_db.roles:
            user_db.roles.remove(r)
        user_db.roles.append(role)
    # Set name and email
    db_adapter.update_object(user_db,
        username=user_update['username'],
        email=user_update['email']
    )
    db_adapter.commit()
    
    return jsonify(result=None)

@app.route('/admin/user_remove', methods=['POST'])
@admin_required
def admin_user_remove():
    db_adapter = current_app.user_manager.db_adapter
    user_del = json.loads(request.data)
    user_db = db_adapter.get_object(db_adapter.UserClass, user_del['id'])
    
    app.logger.info("Removing user: " + str(user_db.username) + "[" + str(user_db.id) + "]."  + "\n")
    db_adapter.delete_object(user_db)
    db_adapter.commit()
    
    return jsonify(result=None)

