from flask import request, render_template, jsonify
from flask_user import current_user
from flask_user import current_app
from flask_user import login_required

import json

from webrob.app_and_db import app
from webrob.pages.utility import admin_required

@app.route('/admin/users')
@admin_required
def admin_users():
    db_adapter = current_app.user_manager.db_adapter
    users = db_adapter.find_all_objects(db_adapter.UserClass)
    user_names = map(lambda u: str(u.username), users)
    user_ids = map(lambda u: str(u.username), users)
    
    return render_template('admin_users.html', **locals())

@app.route('/admin/user_list', methods=['POST'])
def admin_user_list():
    db_adapter = current_app.user_manager.db_adapter
    users = db_adapter.find_all_objects(db_adapter.UserClass)
    user_list = map(lambda u: {
        'id': str(u.id),
        'username': str(u.username),
        'email': str(u.email)
    }, users)
    return jsonify(users=user_list)

@app.route('/admin/user_save', methods=['POST'])
def admin_user_save():
    db_adapter = current_app.user_manager.db_adapter
    user_update = json.loads(request.data)
    user_db = db_adapter.get_object(db_adapter.UserClass, user_update['id'])
    
    app.logger.info("Updating user: " + str(user_db.username) + "[" + str(user_db.id) + "]."  + "\n")
    db_adapter.update_object(user_db,
        username=user_update['username'],
        email=user_update['email']
    )
    db_adapter.commit()
    
    return jsonify(result=None)
