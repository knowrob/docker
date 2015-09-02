
from flask import session, request, send_from_directory, render_template, jsonify, abort
from flask_user import login_required
from flask_user import current_user
from flask_user import current_app

import os
import json

from webrob.app_and_db import app
from webrob.utility import admin_required
from webrob.models.db import *
from webrob.models.users import *

__author__ = 'danielb@cs.uni-bremen.de'

@app.route('/db/page/user_roles')
@admin_required
def db_page_user_roles():
    return render_template('admin_db_user_roles.html', **locals())

@app.route('/db/find/user_roles', methods=['POST'])
@admin_required
def db_find_user_roles():
    db_adapter = current_app.user_manager.db_adapter
    users = db_adapter.find_all_objects(db_table_class('user'))
    user_roles = []
    for u in users:
        user_roles.append({
            'id': u.id,
            'name': u.username,
            'roles': map(lambda r: {'name': r.name}, u.roles)
        })
    return jsonify(result=user_roles)

@app.route('/db/save/user_roles', methods=['POST'])
@admin_required
def db_save_user_roles():
    data = json.loads(request.data)
    if 'roles' not in data or 'id' not in data:
        app.logger.warn("Invalid input data.")
        return jsonify(result=None)
    db_adapter = current_app.user_manager.db_adapter
    user = db_find(db_table_class('user'), data['id'])
    for r in data['roles']:
        role = db_find_name(db_table_class('role'), r['name'])
        if role!=None: user.roles.append(role)
    db_adapter.commit()
    return jsonify(result=None)

@app.route('/db/page/<table>')
@admin_required
def db_page_route(table):
    table_class = db_table_class(table)
    if table_class==None:
        app.logger.warn("Unable to find table for: " + str(table) + ".")
        abort(404)
    
    columns = db_columns(table_class)
    for c in columns:
        if   str(c['type']) == 'BOOLEAN':  c['type'] = 'boolean'
        elif str(c['type']) == 'DATETIME': c['type'] = 'date'
        elif str(c['type']) == 'INTEGER':  c['type'] = 'number'
        else: c['type'] = 'string'
        
        c['editable'] = c['name'] is not 'id'
        if c['editable']: c['editable'] = 'true'
        else: c['editable'] = 'false'
        
        if c['nullable']: c['nullable'] = 'true'
        else: c['nullable'] = 'false'
    
    return render_template('admin_db_table.html', **locals())

@app.route('/db/find/<table>', methods=['POST'])
@admin_required
def db_find_route(table):
    return jsonify(result=db_find_all(db_table_class(table)))

@app.route('/db/save/<table>', methods=['POST'])
@admin_required
def db_update_route(table):
    data = json.loads(request.data)
    cls = db_table_class(table)
    if data!=None:
        if 'id' in data and db_find(cls, data['id']):
            db_update(cls, data['id'], data)
        else:
            db_create(cls, data)
    return jsonify(result=None)

@app.route('/db/new/<table>', methods=['POST'])
@admin_required
def db_create_route(table):
    data = json.loads(request.data)
    if data!=None:
        db_create(db_table_class(table), data)
    return jsonify(result=None)
 
@app.route('/db/delete/<table>', methods=['POST'])
@admin_required
def db_remove_route(table):
    data = json.loads(request.data)
    cls = db_table_class(table)
    if data!=None and 'id' in data and db_find(cls, data['id']):
        db_remove(cls, data['id'])
    return jsonify(result=None)
    
