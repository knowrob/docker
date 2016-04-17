
from flask import session, request, send_from_directory, render_template, jsonify
from flask_user import login_required
from flask_user import current_user
from flask_user import current_app

import os
import json
import random
import string
import shutil

import StringIO
from ftplib import FTP

from webrob.app_and_db import app
from webrob.utility import admin_required
from webrob.models.experiments import Project, Tag
from webrob.models.db import *

__author__ = 'danielb@cs.uni-bremen.de'

@app.route('/download_episode')
@app.route('/download_episode/<category>/<exp>')
def download_episode(category=None, exp=None):
    if category==None:
        if 'exp-category' in session: category = session['exp-category']
        else: return jsonify(result=None)
    if exp==None:
        if 'exp-name' in session: exp = session['exp-name']
        else: return jsonify(result=None)
    
    data = experiment_load_queries(category, exp)
    if data == None:
        app.logger.info("No episode data available for %s/%s" % (category, exp))
        return jsonify(result=None)
    return jsonify(data)

@app.route('/upload_episode', methods=['POST'])
@app.route('/upload_episode/<category>/<exp>', methods=['POST'])
@admin_required
def upload_episode(category=None, exp=None):
    if category==None:
        if 'exp-category' in session: category = session['exp-category']
        else: return jsonify(result=None)
    if exp==None:
        if 'exp-name' in session: exp = session['exp-name']
        else: return jsonify(result=None)
    data = json.loads(request.data)
    
    experiment_create_directory(category, exp)
    episodeData = experiment_load_queries(category, exp)
    if episodeData != None:
        for key in data: episodeData[key] = data[key]
        experiment_save_queries(category, exp, episodeData)
    else:
        app.logger.info("Can not find " + category + "/" + exp)
    return jsonify(result=None)

@app.route('/download_episode_ftp', methods=['POST'])
@app.route('/download_episode_ftp/<category>/<exp>', methods=['POST'])
def download_episode_ftp(category=None, exp=None):
    if category==None:
        if 'exp-category' in session: category = session['exp-category']
        else: return jsonify(result=None)
    if exp==None:
        if 'exp-name' in session: exp = session['exp-name']
        else: return jsonify(result=None)
    data = json.loads(request.data)
        
    # TODO: error handling!
    ftp = FTP(data['server']) # connect to host, default port
    ftp.login(data['user'], data['pw'])
    ftp.cwd(category+'/'+exp)
    
    outStr = StringIO.StringIO()
    ftp.retrlines('RETR queries.json', outStr.write)
    episode_data_str = outStr.getvalue()
    outStr.close()
    
    ftp.quit()
    
    return jsonify(json.loads(episode_data_str))

@app.route('/upload_episode_ftp', methods=['POST'])
@app.route('/upload_episode_ftp/<category>/<exp>', methods=['POST'])
@admin_required
def upload_episode_ftp(category=None, exp=None):
    if category==None:
        if 'exp-category' in session: category = session['exp-category']
        else: return jsonify(result=None)
    if exp==None:
        if 'exp-name' in session: exp = session['exp-name']
        else: return jsonify(result=None)
    data = json.loads(request.data)['options']
    query_library = json.loads(request.data)['lib']
    app.logger.info(str(query_library))
        
    # TODO: error handling!
    ftp = FTP(data['server']) # connect to host, default port
    ftp.login(data['user'], data['pw'])
    ftp.cwd(category+'/'+exp)
    # read query lib from FTP
    outStr = StringIO.StringIO()
    ftp.retrlines('RETR queries.json', outStr.write)
    episode_data_str = outStr.getvalue()
    outStr.close()
    episode_data = json.loads(episode_data_str)
    # update with request data
    for key in query_library: episode_data[key] = query_library[key]
    # store update library
    query_library_string = json.dumps(episode_data, indent=4, separators=(',', ': '))
    ftp.storbinary('STOR queries.json', io.BytesIO(query_library_string))
    ftp.quit()
    
    return jsonify(result=None)

@app.route('/episode_set/<category>/<episode>')
def episode_set(category, episode):
    session['exp-category'] = category
    session['exp-name'] = episode
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
        if not 'tags' in data['meta']: data['meta']['tags'] = []
        if not 'platforms' in data['meta']: data['meta']['platforms'] = []
        if not 'published' in data['meta']: data['meta']['published'] = 'true'
        
        # ignore unpublished experiments
        if data['meta']['published'] == 'false': continue
        
        data['cat'] = cat
        data['exp'] = exp
        exp_data.append(data)
    return render_template('admin/experiments.html', **locals())

@app.route('/knowrob/exp_data/<category>/<exp>')
@login_required
def episode_data(category, exp):
    create_queries_file(category, exp)
    return send_from_directory('/episodes/'+category+'/'+exp, 'queries.json')

@app.route('/knowrob/exp_del/<cat>/<exp>', methods=['POST'])
@admin_required
def experiment_del(cat, exp):
    root = "/episodes"
    cat_path = os.path.join(root, cat)
    if not os.path.isdir(cat_path): return jsonify(result=None)
    exp_path = os.path.join(cat_path, exp)
    if not os.path.isdir(exp_path): return jsonify(result=None)
    shutil.rmtree(exp_path)
    return jsonify(result=None)

@app.route('/knowrob/exp_move/<cat>/<exp>', methods=['POST'])
@admin_required
def experiment_move(cat, exp):
    data = json.loads(request.data)
    cat_new = data['cat']
    exp_new = data['exp']
    if cat_new==cat and exp_new==exp:
        return jsonify(result=None)
    
    path_old = get_experiment_path(cat,exp)
    path_new = get_experiment_path(cat_new,exp_new)
    if os.path.isfile(path_new):
        app.logger.info("Unable to rename experiment. Experiment with same name already existing.")
        return jsonify(result=None)
    
    os.rename(path_old, path_new)
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
            
        for x in ['projects', 'tags', 'platforms']:
            if not x in data: data[x] = []
            wrappedData = []
            for y in data[x]: wrappedData.append({'name': str(y)})
            data[x] = wrappedData
        
        data['cat'] = cat
        data['exp'] = exp
        exp_data.append(data)
    
    return jsonify(experiments=exp_data)

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
        if category.startswith('.'): continue
        p = os.path.join(root_path, category)
        if not os.path.isdir(p): continue
        
        for experiment in os.listdir(p):
            if experiment.startswith('.'): continue
            out.append((category,experiment))
    
    return out

def get_experiment_path(category, exp):
    return "/episodes/"+category+"/"+exp

def create_queries_file(cat,exp):
    path = get_experiment_path(cat,exp)
    if not os.path.isdir(path): return
    f = os.path.join(path, 'queries.json')
    if os.path.isfile(f): return
    
    data = { "meta": 
      {
        "date": "2015-07-18T12:00:00",
        "name": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
        "description": ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)),
        "tags": [],
        "platforms": []
      },
      "query": [],
      "video": []
    }
    with open(f, 'w') as data_file: json.dump(data, data_file)

def experiment_create_directory(cat,exp):
    root = "/episodes"
    cat_path = os.path.join(root, cat)
    if not os.path.isdir(cat_path): os.mkdir(cat_path)
    exp_path = os.path.join(cat_path, exp)
    if not os.path.isdir(exp_path): os.mkdir(exp_path)
    
def experiment_load_queries(category, exp):
    create_queries_file(category,exp)
    episode_file = "/episodes/"+category+"/"+exp+"/queries.json"
    if not os.path.isfile(episode_file): return None
    data = None
    with open(episode_file) as data_file: data = json.load(data_file)
    return data

def experiment_save_queries(category, exp, data):
    episode_file = "/episodes/"+category+"/"+exp+"/queries.json"
    if not os.path.isfile(episode_file): return None
    app.logger.info("Saving " + episode_file)
    with open(episode_file, 'w') as data_file: json.dump(data, data_file, indent=4)
