
from flask import session, jsonify, request, redirect, render_template, url_for, Markup, send_from_directory
from flask_user import login_required
from flask.ext.misaka import markdown

import os, re
import json

from urlparse import urlparse

from webrob.app_and_db import app, db
from webrob.models.tutorials import read_tutorial_page
from webrob.docker.docker_application import ensure_application_started
from webrob.docker import docker_interface
from webrob.pages.utility import admin_required
from webrob.pages.experiments import *

from utility import *

MAX_HISTORY_LINES = 50

@app.route('/knowrob/static/<path:filename>')
@login_required
def download_static(filename):
    return send_from_directory(os.path.join(app.root_path, "static"), filename)

@app.route('/knowrob/knowrob_data/<path:filename>')
@login_required
def download_logged_image(filename):
    return send_from_directory('/episodes/', filename)

@app.route('/knowrob/episode_data/<category>/<episode>')
@login_required
def episode_data(category, episode):
    return send_from_directory('/episodes/'+category+'/'+episode, 'queries.json')

@app.route('/knowrob/episode_save/', methods=['POST'])
@admin_required
def episode_save():
    if 'episode-category' in session and 'episode' in session:
        category = session['episode-category']
        episode = session['episode']
        episodeDataNew = json.loads(request.data)
        episodeDataOld = experiment_load_queries(category, episode)
        episodeDataOld.update(episodeDataNew)
        experiment_save_queries(category, episode, episodeDataOld)
    return jsonify(result=None)

@app.route('/knowrob/summary_data/<path:filename>')
@login_required
def download_summary_image(filename):
    # TODO migrate summary_data -> users own data container and use docker_interface to retrieve summary!
    return send_from_directory('/home/ros/summary_data/', filename)

@app.route('/knowrob/tutorials/')
@app.route('/knowrob/tutorials/<cat_id>/')
@app.route('/knowrob/tutorials/<cat_id>/<page>')
def tutorials(cat_id='getting_started', page=1):
    session['video'] = 0
    #if not ensure_application_started('knowrob/hydro-knowrob-daemon'):
    #    return redirect(url_for('user.logout'))
    
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = 'tutorials'
    show_south_pane = False
    readonly = True
    authentication = False

    tut = read_tutorial_page(cat_id, page)
    content = markdown(tut.text, fenced_code=True)

    # automatically add event handler for highlighting DOM elements
    tmp = re.findall('<em>(.*?)</em>', str(content))
    for t in tmp:
        if 'hl_' in t:
            text = t.split(' hl_')[0]
            idname = t.split(' hl_')[1]
            content = re.sub('<em>{} hl_{}</em>'.format(text, idname), '<em onmouseover="knowrob.highlight_element(&#39;{0}&#39;, &#39;id&#39;, true)" onmouseout="knowrob.highlight_element(&#39;{0}&#39;, &#39;id&#39;, false)">{1}</em>'.format(idname, text), str(content))
        elif 'hlc_' in t:
            text = t.split(' hlc_')[0]
            classname = t.split(' hlc_')[1]
            content = re.sub('<em>{} hlc_{}</em>'.format(text, classname), '<em onmouseover="knowrob.highlight_element(&#39;{0}&#39;, &#39;class&#39;, true)" onmouseout="knowrob.highlight_element(&#39;{0}&#39;, &#39;class&#39;, false)">{1}</em>'.format(classname, text), str(content))

    # automatically add "ask as query" links after code blocks
    content = re.sub('</code>(\s)?</pre>', "</code></pre><div class='show_code'><a href='#' class='show_code'>Ask as query</a></div>", str(content))
    content = Markup(content)

    # check whether there is another tutorial in this category
    nxt  = read_tutorial_page(cat_id, int(page)+1)
    prev = read_tutorial_page(cat_id, int(page)-1)

    return render_template('knowrob_tutorial.html', **locals())
    
@app.route('/knowrob/')
@app.route('/knowrob/hydro-knowrob-daemon')
@app.route('/knowrob/episode/<category>/<episode>')
@login_required
def knowrob(category=None, episode=None):
    session['video'] = 0
    if not ensure_application_started('knowrob/hydro-knowrob-daemon'):
        return redirect(url_for('user.logout'))
    
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname

    container_name = session['user_container_name']
    if category is not None:
        session['episode-category'] = category.replace("%20", " ")
    if episode is not None:
        session['episode'] = episode
    episode_url = get_experiment_download_url()
    app.logger.warn("episode URL " + str(episode_url))

    return render_template('knowrob_simple.html', **locals())

@app.route('/knowrob/video')
@app.route('/knowrob/video/episode/<category>/<episode>')
@login_required
def video(category=None, episode=None):
    session['video'] = 1
    if not ensure_application_started('knowrob/hydro-knowrob-daemon'):
        return redirect(url_for('user.logout'))
    
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']

    if category is not None:
        session['episode-category'] = category.replace("%20", " ")
    if episode is not None:
        session['episode'] = episode
    episode_url = get_experiment_download_url()
    
    return render_template('video.html', **locals())

@app.route('/knowrob/menu', methods=['POST'])
@app.route('/knowrob/hydro-knowrob-daemon/menu', methods=['POST'])
def menu():
    knowrobUrl = '/knowrob/'
    
    menu_left = [
        ('Knowledge Base', knowrobUrl),
        ('Episode Replay',  knowrobUrl+'video'),
        ('Prolog Editor',  knowrobUrl+'editor')
    ]
    
    if current_user.has_role('ADMIN'):
        menu_left.append(
            ('CHOICES', ('Admin', [('CHOICES', ('Knowrob', [
                ('Tutorials', '/knowrob/admin/tutorials')]))]))
        )
    
    # Maps projects to list of experiments
    episode_choices_map =  {}
    for (category,episode) in get_experiment_list():
        episode_url = get_experiment_url(category,episode)
        
        menu = ''
        if len(category)>0: menu = category
        if not menu in episode_choices_map:
            episode_choices_map[menu] = []
        
        episode_choices_map[menu].append((episode, episode_url))
    
    episode_page = '<div class="mega_menu" id="episode-selection">'
    for category in sorted(episode_choices_map.keys()):
        cat_episodes = episode_choices_map[category]
        cat_episodes = sorted(cat_episodes, key=lambda tup: tup[0])
        div_id = category.lower().replace(' ', '-')
        episode_page += '<div class="mega_menu_column" id="'+div_id+'">'
        episode_page += '<h3 class="category-title">'+category.replace('-',' ')+'</h3>'
        episode_page += '<div class="category-episodes">'
        
        # TODO: make this nicer
        technology_episodes = {}
        for (episode,url) in cat_episodes:
            data = experiment_load_queries(category, episode)
            if data is None:
                app.logger.warn("Failed to load episode " + str((category, episode)))
                continue
            if "meta" not in data:
                app.logger.warn("Meta data missing for episode " + str((category, episode)))
                continue
            meta = data['meta']
            if "name" not in meta or "platforms" not in meta:
                app.logger.warn("Meta data missing for episode " + str((category, episode)))
                continue
            
            for t in meta['platforms'].keys():
                if t not in technology_episodes.keys(): technology_episodes[t] = []
                technology_episodes[t].append((meta['name'], url))
        
        for t in sorted(technology_episodes.keys()):
            episode_page += '<h4 class="technology-title">'+t+'</h4>'
            for (name,url) in technology_episodes[t]:
                episode_page += '<a href="'+ url +'">'+name+'</a>'
        
        episode_page += '</div></div>'
    episode_page += '</div>'
        
    
    #episode_page = '<div class="mega_menu" id="episode_selection">'
    #for proj in episode_choices_map.keys():
    #    episode_page += '<div class="mega_menu_column" id="episodes_'+proj+'">'
    #    episode_page += '<h3 id="project_title"><img height="48" src="/knowrob/static/icons/'+proj+'.png" />'+proj+'</h3>'
    #    
    #    platform_and_name = map(lambda (s,url): (s.split('-'),url), episode_choices_map[proj])
    #    platforms = map(lambda (s,_): s[0].split(','), platform_and_name)
    #    platforms_flat = list(set([val for sublist in platforms for val in sublist]))
    #    platforms_flat.sort()
    #    for p in platforms_flat:
    #        episode_page += '<h4 id="platform_title">'+p+'</h4>'
    #        for i in range(len(platform_and_name)):
    #            if not p in platforms[i]: continue
    #            (name,url) = platform_and_name[i]
    #            episode_page += '<a href="'+ url +'">'+'-'.join(name[1:])+'</a>'
    #    
    #    episode_page += '</div>'
    #episode_page += '</div>'
    
    menu_right = [
        ('CHOICES', ('Episode Selection', [('DIV', episode_page)]))
    ]
    
    return jsonify(menu_left=menu_left, menu_right=menu_right)

def __episode_file__():
    if 'episode' in session:
        return session['episode']
    else:
        return None
    
@app.route('/knowrob/episode_set', methods=['POST'])
@login_required
def episode_set():
    episodeName = json.loads(request.data)['episodeName']
    session['episode'] = expName
    return jsonify(result=None)

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


def get_history_file():
  userDir = get_user_dir()
  return os.path.join(get_user_dir(), "query.history")
