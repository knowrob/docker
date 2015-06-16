from flask import request, render_template, jsonify
from flask_user import current_user
from flask_user import current_app
from flask_user import login_required

import json

from webrob.app_and_db import app
from webrob.pages.utility import admin_required
from webrob.models.users import Role

@app.route('/admin/users')
@admin_required
def admin_users():
    return render_template('admin_users.html', **locals())

@app.route('/admin/roles')
@admin_required
def admin_roles():
    return render_template('admin_roles.html', **locals())

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

@app.route('/admin/role_list', methods=['POST'])
@admin_required
def admin_role_list():
    db_adapter = current_app.user_manager.db_adapter
    roles = db_adapter.find_all_objects(Role)
    role_list = map(lambda r:  {
        'id': str(r.id),
        'name': str(r.name)
    }, roles)
    return jsonify(roles=role_list)

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

@app.route('/admin/role_save', methods=['POST'])
@admin_required
def admin_role_save():
    db_adapter = current_app.user_manager.db_adapter
    role_update = json.loads(request.data)
    role_db = db_adapter.get_object(Role, role_update['id'])
    
    app.logger.info("Updating role: " + str(role_db.name) + "[" + str(role_db.id) + "]."  + "\n")
    # Set name and email
    db_adapter.update_object(role_db,
        name=role_update['name']
    )
    db_adapter.commit()
    
    return jsonify(result=None)

@app.route('/admin/role_new', methods=['POST'])
@admin_required
def admin_role_new():
    db_adapter = current_app.user_manager.db_adapter
    new_role = json.loads(request.data)['name']
    new_role_id = max(map(lambda r: r.id, db_adapter.find_all_objects(Role)))+1
    
    app.logger.info("Creating role with name: " + str(new_role) + "\n")
    
    db_adapter.add_object(Role, id=new_role_id, name=new_role)
    db_adapter.commit()
    return jsonify(result=None)

@app.route('/admin/role_remove', methods=['POST'])
@admin_required
def admin_role_remove():
    db_adapter = current_app.user_manager.db_adapter
    role_del = json.loads(request.data)
    role_db = db_adapter.get_object(Role, role_del['id'])
    
    app.logger.info("Removing role: " + str(role_db.name) + "[" + str(role_db.id) + "]."  + "\n")
    db_adapter.delete_object(role_db)
    db_adapter.commit()
    
    return jsonify(result=None)
