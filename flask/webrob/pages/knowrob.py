
from flask import session, jsonify, request, redirect, render_template, url_for, send_from_directory
from flask_user import login_required

import os
import json
import urllib
import base64
import traceback

from urlparse import urlparse

from webrob.app_and_db import app, db
from webrob.docker.docker_application import ensure_application_started
from webrob.docker import docker_interface
from webrob.docker.docker_interface import file_read
from webrob.utility import *
from webrob.pages.experiments import get_experiment_download_url, get_experiment_list, experiment_load_queries
from webrob.config.settings import MAX_HISTORY_LINES

__author__ = 'danielb@cs.uni-bremen.de'

# TODO: remove "/knowrob" prefix in some routes or replace by "/kb"
@app.route('/static/<path:filename>')
@app.route('/knowrob/static/<path:filename>')
def download_static(filename):
    return send_from_directory(os.path.join(app.root_path, "static"), filename)

@app.route('/episode_data/<path:filename>')
@app.route('/knowrob/knowrob_data/<path:filename>')
def download_logged_image(filename):
    return send_from_directory('/episodes/', filename)

@app.route('/knowrob/local_data/<path:filename>')
def transfer_logged_video(filename):
    # TODO: stream the video
    data = base64.b64encode(file_read(session['user_container_name'], filename))
    return '<video controls><source type="video/mp4" src="data:video/mp4;base64,{}"></video>'.format(urllib.quote(data.rstrip('\n')))
    #return '<a href="data:video/mpeg;base64,{}" download="video.mp4">Download video</a>'.format(urllib.quote(data.rstrip('\n')))

# FIXME: iframe does not work standalone right now, redirect to "/#kb" when used without parent frame
@app.route('/kb/')
@app.route('/knowrob/')
@app.route('/knowrob/exp/<category>/<exp>')
def knowrob(category=None, exp=None):
    if not ensure_application_started('knowrob/hydro-knowrob-daemon'):
        return redirect(url_for('user.logout'))
    session['video'] = False
    return __knowrob_page__('knowrob_simple.html', session['user_container_name'], category, exp)

@app.route('/replay')
@app.route('/video')
@app.route('/video/exp/<category>/<exp>')
def video(category=None, exp=None):
    if not ensure_application_started('knowrob/hydro-knowrob-daemon'):
        return redirect(url_for('user.logout'))
    session['video'] = True
    return __knowrob_page__('video.html', session['user_container_name'], category, exp)

def __knowrob_page__(template, container_name, category=None, exp=None):
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    if category is not None: session['exp-category'] = category
    if exp is not None:      session['exp-name'] = exp
    if 'exp-category' in session: category = session['exp-category']
    if 'exp-name' in session: exp = session['exp-name']
    
    exp_url = get_experiment_download_url()
    return render_template(template, **locals())

@app.route('/knowrob/menu', methods=['POST'])
def menu():
    # Maps projects to list of experiments
    episode_choices_map =  {}
    for (category,exp) in get_experiment_list():
        menu = ''
        if len(category)>0: menu = category
        if not menu in episode_choices_map:
            episode_choices_map[menu] = []
        episode_choices_map[menu].append((exp,category))
    
    episode_page = '<div class="mega_menu" id="episode-selection">'
    for category in sorted(episode_choices_map.keys()):
        cat_episodes = episode_choices_map[category]
        cat_episodes = sorted(cat_episodes, key=lambda tup: tup[0])
        div_id = category.lower().replace(' ', '-')
        episode_page += '<div class="mega_menu_column" id="'+div_id+'">'
        episode_page += '<h3 class="category-title">'+category.replace('-',' ')+'</h3>'
        episode_page += '<div class="category-episodes">'
        
        technology_episodes = {}
        for (exp,category) in cat_episodes:
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
            
            if not 'published' in meta: meta['published'] = 'true'
            if meta['published'] == 'false': continue
            
            for t in meta['platforms']:
                if t not in technology_episodes.keys(): technology_episodes[t] = []
                technology_episodes[t].append((meta['name'], (exp,category)))
        
        for t in sorted(technology_episodes.keys()):
            episode_page += '<h4 class="technology-title">'+t+'</h4>'
            for (name,(exp,category)) in technology_episodes[t]:
                episode_page += '<a style="cursor: pointer" onclick=client.setEpisode("'+ category +'","'+ exp +'")>'+name+'</a>'
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
def add_history_item():
  query = json.loads(request.data)['query']
  hfile = get_history_file()
  # Remove newline characters
  #query.replace("\n", " ")
  
  # Read history
  lines = []
  if os.path.isfile(hfile):
    f = open(hfile)
    lines = f.readlines()
    f.close()
  # Remove old history items
  history = ''.join(lines).split("\n\n")
  history = map(lambda x: x + '\n\n', history)
  # Append the last query
  history.append(query+".")
  
  numLines = len(history)
  history = history[max(0, numLines-MAX_HISTORY_LINES):numLines]
  
  with open(hfile, "w") as f:
    f.writelines(history)
  
  return jsonify(result=None)

@app.route('/knowrob/get_history_item', methods=['POST'])
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
    
    # History items are separated with empty line (\n\n)
    history = ''.join(lines).split("\n\n")
    
    item = history[len(history)-index-1]
    if len(item)>0 and item[len(item)-1]=='\n':
      item = item[:len(item)-1]
    
    return jsonify(item=item, index=index)
  
  else:
    return jsonify(item="", index=-1)

@app.route('/knowrob/admin/cookie')
@login_required
def admin_cookie():
    return render_template('admin/cookie.html', **locals())

@app.route('/logs')
@app.route('/log')
def log():
  logStr = docker_interface.get_container_log(session['user_container_name'])
  return render_template('log.html', log=logStr)

def get_history_file():
  userDir = get_user_dir()
  return os.path.join(get_user_dir(), "query.history")

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    app.logger.error(traceback.format_exc())
    return redirect(url_for('user.login'))
