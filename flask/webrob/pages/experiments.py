
from flask import session, request, send_from_directory, render_template, jsonify
from flask_user import login_required
from flask_user import current_user
from flask_user import current_app

import os
import json

from webrob.app_and_db import app
from webrob.utility import admin_required
from webrob.models.experiments import Project, Tag

__author__ = 'danielb@cs.uni-bremen.de'

@app.route('/admin/projects')
@admin_required
def admin_projects():
    return render_template('admin_projects.html', **locals())

@app.route('/project_list', methods=['POST'])
@login_required
def admin_project_list():
    db_adapter = current_app.user_manager.db_adapter
    projects = db_adapter.find_all_objects(Project)
    project_list = map(lambda r:  {
        'id': str(r.id),
        'name': str(r.name),
        'url': str(r.url)
    }, projects)
    return jsonify(projects=project_list)

@app.route('/admin/project_save', methods=['POST'])
@admin_required
def admin_project_save():
    db_adapter = current_app.user_manager.db_adapter
    project_update = json.loads(request.data)
    project_db = db_adapter.get_object(Project, project_update['id'])
    app.logger.info("Updating project: " + str(project_db.name) + "[" + str(project_db.id) + "]."  + "\n")
    db_adapter.update_object(project_db, name=project_update['name'], url=project_update['url'])
    db_adapter.commit()
    return jsonify(result=None)

@app.route('/admin/project_new', methods=['POST'])
@admin_required
def admin_project_new():
    db_adapter = current_app.user_manager.db_adapter
    new_project_data = json.loads(request.data)
    app.logger.info("Creating project with name: " + str(new_project_data['name']) + "\n")
    db_adapter.add_object(Project, name=new_project_data['name'], url=new_project_data['url'])
    db_adapter.commit()
    return jsonify(result=None)




@app.route('/admin/tags')
@admin_required
def admin_tags():
    return render_template('admin_tags.html', **locals())

@app.route('/tag_list', methods=['POST'])
@login_required
def admin_tag_list():
    db_adapter = current_app.user_manager.db_adapter
    tags = db_adapter.find_all_objects(Tag)
    for t in tags:
        members = [attr for attr in dir(t) if not callable(attr) and not attr.startswith("__")]
        app.logger.info(t.name)
        app.logger.info(str(t.metadata))
        app.logger.info(str(dir(t.metadata)))
        app.logger.info(str(members))
    tag_list = map(lambda r:  {
        'id': str(r.id),
        'name': str(r.name)
    }, tags)
    return jsonify(tags=tag_list)

@app.route('/admin/tag_save', methods=['POST'])
@admin_required
def admin_tag_save():
    db_adapter = current_app.user_manager.db_adapter
    tag_update = json.loads(request.data)
    tag_db = db_adapter.get_object(Tag, tag_update['id'])
    app.logger.info("Updating tag: " + str(tag_db.name) + "[" + str(tag_db.id) + "]."  + "\n")
    db_adapter.update_object(tag_db, name=tag_update['name'])
    db_adapter.commit()
    return jsonify(result=None)

@app.route('/admin/tag_new', methods=['POST'])
@admin_required
def admin_tag_new():
    db_adapter = current_app.user_manager.db_adapter
    new_tag_data = json.loads(request.data)
    app.logger.info("Creating tag with name: " + str(new_tag_data['name']) + "\n")
    db_adapter.add_object(Tag, name=new_tag_data['name'])
    db_adapter.commit()
    return jsonify(result=None)



@app.route('/knowrob/admin/experiments')
@admin_required
def admin_experiments():
    exp_list = get_experiment_list()
    exp_data = []
    for (cat,exp) in exp_list:
        data = experiment_load_queries(cat, exp)
        if data is None:
            data = { 'meta': { 'name': '', 'description': '' }}
            
        if not 'projects' in data['meta']: data['meta']['projects'] = []
        if not 'ieee-tags' in data['meta']: data['meta']['ieee-tags'] = []
        #data['meta']['projects'] = ','.join(data['meta']['projects'])
        #data['meta']['ieee-tags'] = ','.join(data['meta']['ieee-tags'])
        
        platforms = []
        if not 'platforms' in data['meta']: data['meta']['platforms'] = {}
        for x in data['meta']['platforms']: platforms.append(x)
        data['meta']['platforms'] = ','.join(data['meta']['platforms'])
        
        data['cat'] = cat
        data['exp'] = exp
        exp_data.append(data)
    return render_template('admin_experiments.html', **locals())

@app.route('/knowrob/exp_data/<category>/<exp>')
@login_required
def episode_data(category, exp):
    return send_from_directory('/episodes/'+category+'/'+exp, 'queries.json')

@app.route('/knowrob/exp_save/<category>/<exp>', methods=['POST'])
@admin_required
def experiment_save(category, exp):
    data = json.loads(request.data)
    episodeData = experiment_load_queries(category, exp)
    if episodeData != None:
        for key in data: episodeData[key] = data[key]
        experiment_save_queries(category, exp, episodeData)
    return jsonify(result=None)

@app.route('/knowrob/exp_meta_data', methods=['POST'])
@admin_required
def get_exp_meta_data():
    exp_list = get_experiment_list()
    exp_data = []
    for (cat,exp) in exp_list:
        data = experiment_load_queries(cat, exp)
        if data is None:
            data = { 'name': '', 'description': '' }
        else: data = data['meta']
        if not 'projects' in data: data['projects'] = []
        if not 'tags' in data: data['tags'] = []
        #data['meta']['projects'] = ','.join(data['meta']['projects'])
        #data['meta']['tags'] = ','.join(data['meta']['tags'])
        
        platforms = []
        if not 'platforms' in data: data['platforms'] = {}
        for x in data['platforms']: platforms.append(x)
        data['platforms'] = ','.join(data['platforms'])
        
        data['cat'] = cat
        data['exp'] = exp
        exp_data.append(data)
    
    return jsonify(experiments=exp_data)


# TODO redundant below
def get_experiment_url(category, exp):
    if category is not None and exp is not None:
        episode_url = '/knowrob/'
        if 'video' in session and session['video']==True:
            episode_url += 'video/'
        episode_url += 'exp/'
        if len(category)>0: episode_url += category + '/'
        episode_url += exp
        return episode_url
    else:
        return None

def get_experiment_download_url():
    if 'exp-category' in session and 'exp-name' in session:
        episode_url = '/knowrob/exp_data/'
        if len(session['exp-category'])>0: episode_url += session['exp-category'] + '/'
        episode_url += session['exp-name']
        return episode_url
    else:
        return None
 
def get_experiment_list():
    out = []
    root_path = "/episodes"
    
    for category in os.listdir(root_path):
        p = os.path.join(root_path, category)
        if not os.path.isdir(p): continue
        
        for experiment in os.listdir(p):
            out.append((category,experiment))
    
    return out

def get_experiment_path(category, exp):
    return "/episodes/"+category+"/"+exp

def experiment_load_queries(category, exp):
    episode_file = "/episodes/"+category+"/"+exp+"/queries.json"
    if not os.path.isfile(episode_file): return None
    data = None
    with open(episode_file) as data_file: data = json.load(data_file)
    return data

def experiment_save_queries(category, exp, data):
    episode_file = "/episodes/"+category+"/"+exp+"/queries.json"
    if not os.path.isfile(episode_file): return None
    app.logger.info("Saving " + episode_file)
    with open(episode_file, 'w') as data_file: json.dump(data, data_file)
