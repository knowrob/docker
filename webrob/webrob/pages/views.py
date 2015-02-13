
from flask import session, jsonify, request, redirect, render_template, Markup, send_from_directory
from flask_user import login_required
from flask.ext.misaka import markdown

import os, sys, re
import json

from urlparse import urlparse
from urllib import urlopen, urlretrieve

from webrob.app_and_db import app, db
from webrob.pages import api
from webrob.user.knowrob_user import read_tutorial_page

from utility import *

from subprocess import call

MAX_HISTORY_LINES = 50

def is_mesh_url_valid(url):
    return urlopen(url).getcode() == 200

def download_mesh_to_local_cache(src, dst):
    """
    download mesh file via http from trusted host
    that is defined in flask settings.
    """
    dstDir = os.path.dirname(dst)
    p_src, ext = os.path.splitext(src)
    p_dst, ext = os.path.splitext(dst)
    
    if is_mesh_url_valid(src):
        if not os.path.exists(dstDir):
            os.makedirs(dstDir)
        urlretrieve(src,dst)
        
        if ext == ".tif":
            call(["/usr/bin/convert", dst, p_dst+".png"])
        if ext == ".dae":
            call(["/opt/webapp/update-texture-reference", dst])
        
        return True
    else:
        if ext == ".png":
            return download_mesh_to_local_cache(p_src + ".tif", p_dst + ".tif")
        else:
            return False

@app.route('/meshes/<path:mesh>')
@login_required
def download_mesh(mesh):
    meshFile = os.path.join('/home/ros/mesh_data', mesh)
    
    if not os.path.isfile(meshFile):
        for repository in app.config['MESH_REPOSITORIES']:
            sourceFile = repository + mesh
            try:
                if download_mesh_to_local_cache(sourceFile, meshFile):
                    break
            except:
                pass
    
    return send_from_directory(
        os.path.dirname(meshFile),
        os.path.basename(meshFile))

@app.route('/knowrob_data/<path:filename>')
@login_required
def download_logged_image(filename):
  return send_from_directory('/home/ros/knowrob_data/', filename)

@app.route('/tutorials/')
@app.route('/tutorials/<cat_id>/')
@app.route('/tutorials/<cat_id>/<page>')
@login_required
def tutorials(cat_id='getting_started', page=1):
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = 'tutorials'
    show_south_pane = True

    tut = read_tutorial_page(cat_id, page)
    content = markdown(tut['text'], fenced_code=True)

    # automatically add "ask as query" links after code blocks
    content = re.sub('</code>(\s)?</pre>', "</code></pre><div class='show_code'><a href='#' class='show_code'>Ask as query</a></div>", str(content))
    content = Markup(content)

    # check whether there is another tutorial in this category
    nxt  = read_tutorial_page(cat_id, int(page)+1)
    prev = read_tutorial_page(cat_id, int(page)-1)

    return render_template('knowrob_tutorial.html', **locals())

@app.route('/knowrob')
@app.route('/exp/<exp_id>')
@login_required
def knowrob(exp_id=None):
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']
    show_south_pane = True

    # Remember experiment selection
    if exp_id is not None: session['exp'] = exp_id
    # Select a query file
    exp_query_file = None
    if 'exp' in session:
        exp = session['exp']
        if exp is not None: exp_query_file = 'queries-' + exp + '.json'
    # TODO: Allow to select html template using a experiment configuration file

    return render_template('knowrob_simple.html', **locals())

@app.route('/video')
@login_required
def video(exp_id=None):
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']

    # Remember experiment selection
    if exp_id is not None: session['exp'] = exp_id
    # Select a query file
    exp_query_file = None
    if 'exp' in session:
        exp = session['exp']
        if exp is not None: exp_query_file = 'queries-' + exp + '.json'
    
    return render_template('video.html', **locals())

@app.route('/exp_list', methods=['POST'])
@login_required
def exp_list():
    expList = []
    exp_file = None
    if 'exp' in session:
        exp_file = session['exp']
    for f in os.listdir(os.path.join(app.root_path, "static")):
        if f.endswith(".json") and f.startswith("queries-"):
            expList.append( f[len("queries-"):len(f)-len(".json")] )
    return jsonify(result=expList, selection=exp_file)

@app.route('/exp_set', methods=['POST'])
@login_required
def exp_set():
    expName = json.loads(request.data)['experimentName']
    session['exp'] = expName
    return jsonify(result=None)

@app.route('/add_history_item', methods=['POST'])
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

@app.route('/get_history_item', methods=['POST'])
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

@app.route('/create_api_token', methods=['GET'])
@login_required
def create_api_token():
    api.create_token()
    return redirect('/')

def get_history_file():
  userDir = get_user_dir()
  return os.path.join(get_user_dir(), "query.history")
