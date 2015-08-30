
import os, sys
import json
import zipfile

from urlparse import urlparse

from flask import session, request, render_template, jsonify, send_file
from flask_user import login_required

from webrob.app_and_db import app
from webrob.docker import docker_interface
from webrob.docker.docker_interface import LFTransfer
from webrob.utility import copy_template_file

__author__ = 'danielb@cs.uni-bremen.de'

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
    packageName = json.loads(request.data)['packageName']
    
    # Create package root directory
    if docker_interface.file_exists(session['user_container_name'], packageName):
        app.logger.warning("Package already exists.")
        return jsonify(result=None)
    
    # Make sure templates are available
    templatePath = os.path.abspath('webrob/templates/package')
    if not os.path.exists(templatePath):
        app.logger.warning("Package templates missing at " + templatePath + ".")
        return jsonify(result=None)

    try:
        with LFTransfer(session['user_container_name']) as lft:
            pkgPath = os.path.join(lft.get_filetransfer_folder(), packageName)
            # Copy package template to user_data container while replacing some keywords
            for root, dirs, files in os.walk(templatePath):
                for f in files:
                    abs_p = os.path.join(root, f)
                    rel_p = os.path.relpath(abs_p, templatePath)
                    user_p = os.path.join(pkgPath, rel_p)
                    copy_template_file(abs_p, user_p, {
                        "pkgName": packageName,
                        "userName": session['user_container_name']
                    })
            lft.to_container(packageName, packageName)
    except:  # catch *all* exceptions
        app.logger.error(str(sys.exc_info()[0]))
        pkg_del(packageName)
    
    return jsonify(result=None)

@app.route('/knowrob/pkg_del', methods=['POST'])
@login_required
def pkg_del(packageName=None):
    pkgName = packageName
    if pkgName is None:
        pkgName = session['pkg']
    docker_interface.file_rm(session['user_container_name'], pkgName, True)
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
    files = filter(lambda s: s['isdir'], docker_interface.file_ls(session['user_container_name'], '.')['children'])
    filenames = map(lambda s: s['name'], files)
    return jsonify(result=filenames)

@app.route('/knowrob/pkg_read', methods=['POST'])
@login_required
def pkg_read():
    path = get_file_path(json.loads(request.data)['file'])
    # Read the file
    content = docker_interface.file_read(session['user_container_name'], path).splitlines(True)
    return jsonify(result=content)

@app.route('/knowrob/pkg_down', methods=['POST'])
@login_required
def pkg_down():
    with LFTransfer(session['user_container_name']) as lft:
        name = session['pkg']
        zipName = session['pkg'] + '.zip'
        lft.from_container(name, name)
        pkgPath = os.path.join(lft.get_filetransfer_folder(), name)
        zipPath = os.path.join(lft.get_filetransfer_folder(), zipName)
        zipf = zipfile.ZipFile(zipPath, 'w')
        zipdir(pkgPath, lft.get_filetransfer_folder(), zipf)
        zipf.close()
        return send_file(zipPath,
                         mimetype="application/zip",
                         as_attachment=True,
                         attachment_filename=zipName)

@app.route('/knowrob/file_write', methods=['POST'])
@login_required
def file_write():
    data = json.loads(request.data)
    path = get_file_path(data['file'])
    docker_interface.file_write(session['user_container_name'], data['content'], path)
    
    return jsonify(result=None)
   
@app.route('/knowrob/file_del', methods=['POST'])
@login_required 
def file_del():
    path = get_file_path(json.loads(request.data)['file'])
    docker_interface.file_rm(session['user_container_name'], path, True)
    
    return get_pkg_tree()

 
def get_file_path(fileName):
    """
    Selects package subdir based on file extension.
    """
    path = session['pkg']
    (_, ext) = os.path.splitext(fileName)
    if ext == ".pl":
        path = os.path.join(path, "prolog")
    elif ext == ".owl":
        path = os.path.join(path, "owl")
    return os.path.join(path, fileName)

def get_pkg_tree():
    # List files in package dir
    pkgPath = session['pkg']
    rootFiles = docker_interface.file_ls(session['user_container_name'], pkgPath, True)['children']
    # Return list of files
    return jsonify(result=rootFiles)

def zipdir(path, pathPrefix, zipFile):
    for root, dirs, files in os.walk(path):
        for f in files:
            abs_p = os.path.join(root, f)
            rel_p = os.path.relpath(abs_p, pathPrefix)
            zipFile.write(abs_p, rel_p)
