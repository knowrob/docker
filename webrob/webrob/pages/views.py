
from flask import Flask, session, jsonify, url_for, escape, request, make_response, render_template, g, abort, flash, Markup, send_file, send_from_directory, current_app, redirect
from flask_user import current_user, login_required
from flask.ext.misaka import markdown
from flask.ext.mail import Mail
from flask.ext.user import current_user, login_required, roles_required, SQLAlchemyAdapter, UserManager, UserMixin
from flask.ext.user.signals import user_logged_in
from flask.ext.user.signals import user_logged_out
from flask.ext.user.forms import RegisterForm
from werkzeug import secure_filename

import os
import hashlib
import json

import random
import string
import time
import sys
import re
import shutil
import zipfile

from wtforms import validators
from wtforms import StringField
from wtforms import SelectField
from wtforms.validators import Required

from webrob.app_and_db import app, db
from webrob.docker import knowrob_docker
from webrob.user import knowrob_user

from urlparse import urlparse

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Knowrob package templates
    
PACKAGE_XML_TXT ="""<package>
  <name>{pkgName}</name>
  
  <version>1.0.0</version>
  
  <description>{pkgName} user package</description>
  
  <maintainer>{userName}</maintainer>
  
  <license>GPL</license>
  
  <url type="website">http://www.knowrob.org/</url>
  
  <author>{userName}</author>
  
  <buildtool_depend>catkin</buildtool_depend>
  
  <build_depend>knowrob_common</build_depend>
  
  <run_depend>knowrob_common</run_depend>
  
</package>"""

CMAKE_LIST_TXT ="""cmake_minimum_required(VERSION 2.8.3)

project({pkgName})

find_package(catkin REQUIRED COMPONENTS knowrob_common)

catkin_package(
    DEPENDS knowrob_common
)"""

PROLOG_INIT_TXT ="""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% dependencies
:- register_ros_package(knowrob_common).
:- register_ros_package(knowrob_srdl).
:- register_ros_package(knowrob_cram).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Include source files
%:- use_module(library('test')).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% parse OWL files, register name spaces
% :- owl_parser:owl_parse('package://{pkgName}/owl/dummy.owl').
% :- rdf_db:rdf_register_ns(dummy, 'http://knowrob.org/kb/dummy.owl#', [keep(true)])."""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Web stuff

@user_logged_in.connect_via(app)
def track_login(sender, user, **extra):
    session['user_container_name'] = user.username
    session['username'] = user.username
    session['user_data_container_name'] = "user_data"
    session['common_data_container_name'] = "knowrob_data"
    session['exp'] = None
    session['user_home_dir'] = '/home/ros/user_data/' + session['user_container_name']
    session['rosauth_mac'] = generate_mac()
    session['show_loading_overlay'] = True
    if not 'pkg' in session: session['pkg'] = ''
    knowrob_docker.start_container()
    #sender.logger.info('user logged in')

@user_logged_out.connect_via(app)
def track_logout(sender, user, **extra):
    knowrob_docker.stop_container()
    #sender.logger.info('user logged out')


@app.route('/')
def show_user_data():
    if not current_user.is_authenticated():
        return redirect(url_for('user.login'))
    #get_user_data(current_user.username)
    print request.host


    overlay = None
    if(session.get('show_loading_overlay') == True):
        overlay = True
        session.pop('show_loading_overlay')

    return render_template('show_user_data.html', overlay=overlay)


#@app.route('/ws/<user_id>/')
#def ws_url(user_id=None):
  # dummy method to define endpoint; will be re-routed by reverse proxy
  # to the websockets endpoints
  #return




@app.route('/pr2_description/meshes/<path:filename>')
def download_mesh(filename):
  return send_from_directory('/opt/webapp/pr2_description/meshes/', filename, as_attachment=True)

@app.route('/knowrob_data/<path:filename>')
def download_logged_image(filename):
  return send_from_directory('/home/ros/knowrob_data/', filename)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != "" and request.form['password'] != ""):
            if is_valid_user(request.form['username'], request.form['password']):

                session['username'] = request.form['username']
                session['pkg'] = ""
                session['exp'] = None

                session['user_container_name'] = session['username']
                session['user_data_container_name'] = session['username'] + "_data"
                session['common_data_container_name'] = "knowrob_data"

                session['logged_in'] = True
                session['rosauth_mac'] = generate_mac()
                flash('You were logged in')

                session['show_loading_overlay'] = True

                knowrob_docker.start_container()
                return redirect(url_for('show_user_data'))
            else :
                error = 'Invalid user data'
    return render_template('login.html', error=error, action="login")

@app.route('/logout')
def logout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    session.pop('logged_in', None)
    knowrob_docker.stop_container()
    flash('You were logged out')
    return redirect(url_for('show_user_data'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':

        if (request.form['username'] == ""):
            error = 'Please specify a user name.'

        elif (request.form['password'] == ""):
            error = 'Please specify a password'

        elif(request.form['email'] == ""):
            error = 'Please specify an email address.'

        elif(user_exists(request.form['username'])):
            error = 'This username already exists. Please choose another username.'

        else:
            insert_user(request.form['username'], request.form['password'], request.form['email'])
            session['username'] = request.form['username']

            session['user_container_name'] = session['username']
            session['user_data_container_name'] = session['username'] + "_data"
            session['common_data_container_name'] = "knowrob_data"

            session['logged_in'] = True
            session['rosauth_mac'] = generate_mac()
            #create_data_containers()
            start_container()

            session['show_loading_overlay'] = True
            return redirect(url_for('show_user_data'))

    return render_template('login.html', error=error, action="register")



@app.route('/tutorials/')
@app.route('/tutorials/<cat_id>/')
@app.route('/tutorials/<cat_id>/<page>')
@login_required
def tutorials(cat_id='getting_started', page=1):

    #if not session.get('logged_in'):
    #    return redirect(url_for('login'))

    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = 'tutorials'

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
    #if not session.get('logged_in'):
    #    return redirect(url_for('login'))
    error=""
    #current_app.logger.debug(request)
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

    return render_template('knowrob_simple.html', **locals())
    
###########################
############# Editor Begin
###########################
    
@app.route('/editor')
@login_required
def editor(filename=""):
    return render_template('editor.html')

@app.route('/pkg_new', methods=['POST'])
@login_required
def pkg_new():
    packageName = json.loads(request.data)['packageName'];
    pkgPath = os.path.join(getUserDir(), packageName)
    
    # Create package root directory
    if os.path.exists(pkgPath):
        sys.stderr.write("Package already exists.\n")
        return None
    os.makedirs(pkgPath)
    
    session['pkg'] = packageName
    
    # Create package.xml
    pkgXml = PACKAGE_XML_TXT.format(
        pkgName= packageName,
        userName= session['user_container_name']
    )
    pkgXmlFile = os.path.join(pkgPath, 'package.xml')
    writeTextFile(pkgXmlFile, pkgXml)
    
    # Create CMakeList
    cmakeList = CMAKE_LIST_TXT.format(
        pkgName= packageName
    )
    cmakeListFile = os.path.join(pkgPath, 'CMakeLists.txt')
    writeTextFile(cmakeListFile, cmakeList)
    
    prologDir = os.path.join(pkgPath, 'prolog')
    # Create prolog/owl directories
    os.makedirs(prologDir)
    os.makedirs(os.path.join(pkgPath, 'owl'))
    
    # Create prolog init file
    prologInit = PROLOG_INIT_TXT.format(
        pkgName= packageName
    )
    prologInitFile = os.path.join(prologDir, 'init.pl')
    writeTextFile(prologInitFile, prologInit)
    
    return jsonify(result=None)

@app.route('/pkg_del', methods=['POST'])
@login_required
def pkg_del():
    shutil.rmtree(os.path.join(getUserDir(), session['pkg']))
    return jsonify(result=None)

@app.route('/pkg_set', methods=['POST'])
@login_required
def pkg_set():
    # Update package name
    data = json.loads(request.data)
    if 'packageName' in data and len(data['packageName'])>0:
        session['pkg'] = data['packageName']
    return getPkgTree()

@app.route('/pkg_list', methods=['POST'])
@login_required
def pkg_list():
    # Return list of packages
    files = filter(lambda f: os.path.isdir(os.path.join(getUserDir(), f)), os.listdir(getUserDir()))
    return jsonify(result=files)

@app.route('/pkg_read', methods=['POST'])
@login_required
def pkg_read():
    path = getFilePath(json.loads(request.data)['file'])
    
    # Read the file
    f = open(path, 'r')
    content = f.readlines()
    f.close()
    
    return jsonify(result=content)

@app.route('/pkg_down', methods=['POST'])
@login_required
def pkg_down():
    path = os.path.join(getUserDir(), session['pkg'])
    
    zipName = session['pkg'] + '.zip'
    zipPath = os.path.join(getUserDir(), zipName)
    zipf = zipfile.ZipFile(zipPath, 'w')
    zipdir(path, getUserDir(), zipf)
    zipf.close()
    # FIXME: zip file never removed!
    
    return send_file(zipPath, 
         mimetype="application/zip", 
         as_attachment=True, 
         attachment_filename=zipName)

@app.route('/file_write', methods=['POST'])
@login_required
def file_write():
    data = json.loads(request.data)
    path = getFilePath(data['file'])
    
    writeTextFile(path, data['content'])
    
    return jsonify(result=None)
   
@app.route('/file_del', methods=['POST'])
@login_required 
def file_del():
    path = getFilePath(json.loads(request.data)['file'])
    
    if(os.path.isfile(path)):
        os.remove(path)
    
    return getPkgTree()
    
###########################
############# Editor End
###########################
    
###########################
############# Logging Begin
###########################

@app.route('/log')
def log():
  c = knowrob_docker.docker_connect()
  container_id = session['user_container_name']
  logger = c.logs(container_id, stdout=True, stderr=True, stream=False, timestamps=False)
  
  logStr = ""
  for c in logger: logStr += c
  
  return render_template('log.html', log=logStr)

###########################
############# Logging End
###########################
  
    
###########################
############# Utility Begin
###########################

def getUserDir():
    userDir = "/home/ros/user_data/" + session['user_container_name']
    if not os.path.exists(userDir):
        print("Creating user directory at " + userDir)
        os.makedirs(userDir)
    return userDir

def writeTextFile(path, content):
    f = open(path, "w")
    f.write(content)
    f.close()

def getFilePath(fileName):
    path = os.path.join(getUserDir(), session['pkg'])
    (_, ext) = os.path.splitext(fileName)
    if(ext == ".pl"):
        path = os.path.join(path, "prolog")
    elif(ext == ".owl"):
        path = os.path.join(path, "owl")
    return os.path.join(path, fileName)
 
def getPkgTree():
    # List files in package dir
    pkgPath = os.path.join(getUserDir(), session['pkg'])
    rootFiles = listPkgFiles(session['pkg'], pkgPath)['children']
    # Return list of files
    return jsonify(result=rootFiles)

def getPackageFiles():
    if not 'pkg' in session.keys(): return []
    
    packageName = session['pkg'];
    pkgPath = os.path.join(getUserDir(), packageName)
    
    files = []
    for root, _, x in os.walk(pkgPath):
        for f in x:
            p = os.path.join(root, f)
            files.append(p[p.find('/'+packageName):])
    return files
    
def listPkgFiles(name, root):
    out = []
    
    if os.path.isdir(root):
        for child in os.listdir(root):
            out.append(listPkgFiles(child, os.path.join(root,child)))
    
    return {'name': name, 'children': out, 'isdir': os.path.isdir(root)}

def zipdir(path, pathPrefix, zipFile):
    for root, dirs, files in os.walk(path):
        for f in files:
            abs_p = os.path.join(root, f)
            rel_p = os.path.relpath(abs_p, pathPrefix)
            zipFile.write(abs_p, rel_p)
    
def generate_mac():

    secret = "RW6WZ2yp67ETMdj2"
    client = request.remote_addr
    dest   = request.host_url # TODO: find out the actual IP; this will return the hostname

    rand = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(30)])

    t = int(time.time())
    level = "user"
    end = int(t + 3600)

    mac = hashlib.sha512(secret + client + dest + rand + str(t) + level + str(end) ).hexdigest()

    return "ros.authenticate(" + mac + ", " + client + ", " + dest + ", " + rand + ", " + str(t) + ", " + level + ", " + str(end) + ")"
    
###########################
############# Utility End
###########################

