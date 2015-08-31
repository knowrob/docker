
from flask import session, jsonify, request, redirect, render_template, url_for, send_from_directory
from flask_user import login_required

import os
import json

from urlparse import urlparse

from webrob.app_and_db import app, db
from webrob.docker.docker_application import ensure_application_started
from webrob.docker import docker_interface
from webrob.utility import *
from webrob.pages.experiments import get_experiment_download_url, get_experiment_url, get_experiment_list, experiment_load_queries

__author__ = 'danielb@cs.uni-bremen.de'

MAX_HISTORY_LINES = 50

@app.route('/knowrob/static/<path:filename>')
@login_required
def download_static(filename):
    return send_from_directory(os.path.join(app.root_path, "static"), filename)

@app.route('/knowrob/knowrob_data/<path:filename>')
@login_required
def download_logged_image(filename):
    return send_from_directory('/episodes/', filename)
    
@app.route('/knowrob/')
@app.route('/knowrob/exp/<category>/<exp>')
@login_required
def knowrob(category=None, exp=None):
    session['video'] = False
    return __knowrob_page__('knowrob_simple.html', category, exp)

@app.route('/knowrob/video')
@app.route('/knowrob/video/exp/<category>/<exp>')
@login_required
def video(category=None, exp=None):
    session['video'] = True
    return __knowrob_page__('video.html', category, exp)

def __knowrob_page__(template, category=None, exp=None):
    if not ensure_application_started('knowrob/hydro-knowrob-daemon'):
        return redirect(url_for('user.logout'))
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']
    if category is not None: session['exp-category'] = category
    if exp is not None:      session['exp-name'] = exp
    exp_url = get_experiment_download_url()
    return render_template(template, **locals())

@app.route('/knowrob/menu', methods=['POST'])
def menu():
    # Maps projects to list of experiments
    episode_choices_map =  {}
    for (category,exp) in get_experiment_list():
        episode_url = get_experiment_url(category,exp)
        
        menu = ''
        if len(category)>0: menu = category
        if not menu in episode_choices_map:
            episode_choices_map[menu] = []
        
        episode_choices_map[menu].append((exp, episode_url))
    
    episode_page = '<div class="mega_menu" id="episode-selection">'
    for category in sorted(episode_choices_map.keys()):
        cat_episodes = episode_choices_map[category]
        cat_episodes = sorted(cat_episodes, key=lambda tup: tup[0])
        div_id = category.lower().replace(' ', '-')
        episode_page += '<div class="mega_menu_column" id="'+div_id+'">'
        episode_page += '<h3 class="category-title">'+category.replace('-',' ')+'</h3>'
        episode_page += '<div class="category-episodes">'
        
        technology_episodes = {}
        for (exp,url) in cat_episodes:
            data = experiment_load_queries(category, exp)
            if data is None:
                app.logger.warn("Failed to load episodes for " + str((category, exp)))
                continue
            if "meta" not in data:
                app.logger.warn("Meta data missing for episodes for " + str((category, exp)))
                continue
            meta = data['meta']
            if "name" not in meta or "platforms" not in meta:
                app.logger.warn("Meta data missing for episodes for " + str((category, exp)))
                continue
            
            for t in meta['platforms']:
                if t not in technology_episodes.keys(): technology_episodes[t] = []
                technology_episodes[t].append((meta['name'], url))
        
        for t in sorted(technology_episodes.keys()):
            episode_page += '<h4 class="technology-title">'+t+'</h4>'
            for (name,url) in technology_episodes[t]:
                episode_page += '<a href="'+ url +'">'+name+'</a>'
        episode_page += '</div></div>'
    episode_page += '</div>'
    
    menu_left = []
    menu_right = [{
        'text': 'Episode Selection',
        'submenu': [{
            'text': '',
            'submenu_page': episode_page
        }]
    }]
    
    return jsonify(menu_left=menu_left, menu_right=menu_right)

@app.route('/knowrob/add_history_item', methods=['POST'])
@login_required
def add_history_item():
  query = json.loads(request.data)['query']
  hfile = get_history_file()
  # Remove newline characters
  query.replace("\n", " ")
  
  # Read history
  lines = []
  if os.path.isfile(hfile):
    f = open(hfile)
    lines = f.readlines()
    f.close()
  # Append the last query
  lines.append(query+".\n")
  # Remove old history items
  numLines = len(lines)
  lines = lines[max(0, numLines-MAX_HISTORY_LINES):numLines]
  
  with open(hfile, "w") as f:
    f.writelines(lines)
  
  return jsonify(result=None)

@app.route('/knowrob/get_history_item', methods=['POST'])
@login_required
def get_history_item():
  index = json.loads(request.data)['index']
  
  if index<0:
    return jsonify(item="", index=-1)
  
  hfile = get_history_file()
  if os.path.isfile(hfile):
    # Read file content
    f = open(hfile)
    lines = f.readlines()
    f.close()
    
    # Clamp index
    if index<0: index=0
    if index>=len(lines): index=len(lines)-1
    if index<0: return jsonify(item="", index=-1)
    
    item = lines[len(lines)-index-1]
    item = item[:len(item)-1]
    
    return jsonify(item=item, index=index)
  
  else:
    return jsonify(item="", index=-1)

@app.route('/log')
@login_required
def log():
    logStr = docker_interface.get_container_log(session['user_container_name'])
    return render_template('log.html', log=logStr)

def get_history_file():
  userDir = get_user_dir()
  return os.path.join(get_user_dir(), "query.history")
