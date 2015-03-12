#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# @author Daniel Beßler

import os, sys, shutil
import json
import zipfile

from urlparse import urlparse

from flask import session, request, render_template, jsonify, send_file
from flask_user import login_required

# TODO: use this somewhere?
from werkzeug import secure_filename

from webrob.app_and_db import app
from utility import *
    
@app.route('/knowrob/editor')
@login_required
def editor(filename=""):
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']
    
    return render_template('editor.html', **locals())

@app.route('/knowrob/pkg_new', methods=['POST'])
@login_required
def pkg_new():
    packageName = json.loads(request.data)['packageName'];
    pkgPath = os.path.join(get_user_dir(), packageName)
    
    # Create package root directory
    if os.path.exists(pkgPath):
        app.logger.warning("Package already exists.")
        return jsonify(result=None)
    
    # Make sure templates are available
    templatePath = os.path.abspath('webrob/templates/package')
    if not os.path.exists(templatePath):
        app.logger.warning("Package templates missing at " + templatePath + ".")
        return jsonify(result=None)
    
    try:
      os.makedirs(pkgPath)
      
      # Copy package template to user_data container while replacing some keywords
      for root, dirs, files in os.walk(templatePath):
          for f in files:
              abs_p = os.path.join(root, f)
              rel_p = os.path.relpath(abs_p, templatePath)
              user_p = os.path.join(pkgPath, rel_p)
              copy_template_file(abs_p, user_p, {
                "pkgName":packageName,
                "userName":session['user_container_name']
              })
    except: # catch *all* exceptions
        app.logger.error(str(sys.exc_info()[0]))
        pkg_del(packageName)
    
    return jsonify(result=None)

@app.route('/knowrob/pkg_del', methods=['POST'])
@login_required
def pkg_del(packageName=None):
    pkgName = packageName
    if pkgName==None: pkgName = session['pkg']
    
    shutil.rmtree(os.path.join(get_user_dir(), pkgName))
    return jsonify(result=None)

@app.route('/knowrob/pkg_set', methods=['POST'])
@login_required
def pkg_set():
    # Update package name
    data = json.loads(request.data)
    if 'packageName' in data and len(data['packageName'])>0:
        session['pkg'] = data['packageName']
    return get_pkg_tree()

@app.route('/knowrob/pkg_list', methods=['POST'])
@login_required
def pkg_list():
    # Return list of packages
    files = filter(lambda f: os.path.isdir(os.path.join(get_user_dir(), f)), os.listdir(get_user_dir()))
    return jsonify(result=files)

@app.route('/knowrob/pkg_read', methods=['POST'])
@login_required
def pkg_read():
    path = get_file_path(json.loads(request.data)['file'])
    
    # Read the file
    f = open(path, 'r')
    content = f.readlines()
    f.close()
    
    return jsonify(result=content)

@app.route('/knowrob/pkg_down', methods=['POST'])
@login_required
def pkg_down():
    path = os.path.join(get_user_dir(), session['pkg'])
    
    zipName = session['pkg'] + '.zip'
    zipPath = os.path.join(get_user_dir(), zipName)
    zipf = zipfile.ZipFile(zipPath, 'w')
    zipdir(path, get_user_dir(), zipf)
    zipf.close()
    # FIXME: zip file never removed!
    
    return send_file(zipPath, 
         mimetype="application/zip", 
         as_attachment=True, 
         attachment_filename=zipName)

@app.route('/knowrob/file_write', methods=['POST'])
@login_required
def file_write():
    data = json.loads(request.data)
    path = get_file_path(data['file'])
    
    write_text_file(path, data['content'])
    
    return jsonify(result=None)
   
@app.route('/knowrob/file_del', methods=['POST'])
@login_required 
def file_del():
    path = get_file_path(json.loads(request.data)['file'])
    
    if(os.path.isfile(path)):
        os.remove(path)
    
    return get_pkg_tree()

#################################
#################################
#################################
 
def get_file_path(fileName):
    """
    Selects package subdir based on file extension.
    """
    path = os.path.join(get_user_dir(), session['pkg'])
    (_, ext) = os.path.splitext(fileName)
    if(ext == ".pl"):
        path = os.path.join(path, "prolog")
    elif(ext == ".owl"):
        path = os.path.join(path, "owl")
    return os.path.join(path, fileName)

def get_pkg_tree():
    # List files in package dir
    pkgPath = os.path.join(get_user_dir(), session['pkg'])
    rootFiles = list_pkg_files(session['pkg'], pkgPath)['children']
    # Return list of files
    return jsonify(result=rootFiles)
    
def list_pkg_files(name, root):
    out = []
    if os.path.isdir(root):
        for child in os.listdir(root):
            out.append(list_pkg_files(child, os.path.join(root,child)))
    return {'name': name, 'children': out, 'isdir': os.path.isdir(root)}

def zipdir(path, pathPrefix, zipFile):
    for root, dirs, files in os.walk(path):
        for f in files:
            abs_p = os.path.join(root, f)
            rel_p = os.path.relpath(abs_p, pathPrefix)
            zipFile.write(abs_p, rel_p)
