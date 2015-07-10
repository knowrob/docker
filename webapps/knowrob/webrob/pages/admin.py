
from flask import request, render_template, jsonify
from flask_user import current_app
import json

from webrob.models.tutorials import Tutorial
from webrob.app_and_db import app
from webrob.pages.utility import admin_required

@app.route('/knowrob/admin/tutorials')
@admin_required
def admin_tutorials():
    return render_template('admin_tutorials.html', **locals())

@app.route('/knowrob/admin/tutorial_list', methods=['POST'])
@admin_required
def admin_tutorial_list():
    db_adapter = current_app.user_manager.db_adapter
    tutorials = db_adapter.find_all_objects(Tutorial)
    tut_list = map(lambda r:  {
        'id': str(r.id),
        'cat_id': str(r.cat_id),
        'cat_title': str(r.cat_title),
        'title': str(r.title),
        'text': str(r.text),
        'page': str(r.page)
    }, tutorials)
    return jsonify(tutorials=tut_list)

def find_cat_id(title):
    db_adapter = current_app.user_manager.db_adapter
    tutorials = db_adapter.find_all_objects(Tutorial)
    for t in tutorials:
        if str(t.cat_title) == title: return str(t.cat_id)
    return None

@app.route('/knowrob/admin/tutorial_save', methods=['POST'])
@admin_required
def admin_tutorial_save():
    db_adapter = current_app.user_manager.db_adapter
    tut_update = json.loads(request.data)
    tut_db = db_adapter.get_object(Tutorial, tut_update['id'])
    
    db_adapter.update_object(tut_db,
        cat_id = find_cat_id( tut_update['cat_title'] ),
        cat_title = tut_update['cat_title'],
        title = tut_update['title'],
        text = tut_update['text'],
        page = tut_update['page']
    )
    db_adapter.commit()
    
    return jsonify(result=None)

@app.route('/knowrob/admin/tutorial_new', methods=['POST'])
@admin_required
def admin_tutorial_new():
    db_adapter = current_app.user_manager.db_adapter
    new_tut = json.loads(request.data)
    
    app.logger.info("Creating tutorial with title: " + new_tut['title'] + "\n")
    
    db_adapter.add_object(Tutorial,
        cat_id = find_cat_id( new_tut['cat_title'] ),
        cat_title = new_tut['cat_title'],
        title = new_tut['title'],
        text = new_tut['text'],
        page = new_tut['page']
    )
    db_adapter.commit()
    return jsonify(result=None)

@app.route('/knowrob/admin/tutorial_remove', methods=['POST'])
@admin_required
def admin_tutorial_remove():
    db_adapter = current_app.user_manager.db_adapter
    tut_del = json.loads(request.data)
    tut_db = db_adapter.get_object(Tutorial, tut_del['id'])
    
    app.logger.info("Removing tutorial: " + str(tut_db.title) + "[" + str(tut_db.id) + "]."  + "\n")
    db_adapter.delete_object(tut_db)
    db_adapter.commit()
    
    return jsonify(result=None)
