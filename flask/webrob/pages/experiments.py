
from flask import session, request, send_from_directory, render_template, jsonify
from flask_user import login_required
from flask_user import current_user
from flask_user import current_app

import os
import json

from webrob.app_and_db import app
from webrob.utility import admin_required
from webrob.models.experiments import Project, Tag
from webrob.models.db import *

__author__ = 'danielb@cs.uni-bremen.de'

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
        if not 'tags' in data['meta']: data['meta']['tags'] = []
        if not 'platforms' in data['meta']: data['meta']['platforms'] = []
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
        else:
            data = data['meta']
        if not 'projects' in data: data['projects'] = []
        if not 'tags' in data: data['tags'] = []
        if not 'platforms' in data: data['platforms'] = []
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
