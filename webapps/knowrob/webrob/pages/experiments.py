
from flask import session, send_from_directory
from flask_user import login_required

import os
import json

from webrob.app_and_db import app
from webrob.pages.utility import admin_required

@app.route('/knowrob/exp_data/<category>/<exp>')
@login_required
def episode_data(category, exp):
    return send_from_directory('/episodes/'+category+'/'+exp, 'queries.json')

@app.route('/knowrob/exp_save', methods=['POST'])
@admin_required
def experiment_save():
    if 'exp-category' in session and 'exp-name' in session:
        category = session['exp-category']
        exp = session['exp-name']
        data = json.loads(request.data)
        episodeData = experiment_load_queries(category, exp)
        for key in data: episodeData[key] = data[key]
        experiment_save_queries(category, exp, episodeData)
    return jsonify(result=None)

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
