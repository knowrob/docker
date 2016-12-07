
import os, sys
import json
import zipfile
import traceback

from urlparse import urlparse

from flask import session, request, render_template, jsonify, send_file, redirect, url_for
from flask_user import login_required
from flask_user import current_app

from webrob.app_and_db import app
from webrob.docker import docker_interface
from webrob.docker.docker_interface import LFTransfer
from webrob.utility import copy_template_file
from webrob.docker.docker_application import ensure_application_started

from webrob.models.teaching import CourseExercise

__author__ = 'danielb@cs.uni-bremen.de'

@app.route('/editor')
def editor(filename=""):
    if not ensure_application_started('knowrob/hydro-knowrob-daemon'):
        return redirect(url_for('user.logout'))
    
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']
    
    return render_template('editor.html', **locals())

@app.route('/pkg/new', methods=['POST'])
def pkg_new():
    packageName = json.loads(request.data)['packageName']
    
    if docker_interface.file_exists(session['user_container_name'], packageName):
        app.logger.warning("Package already exists.")
        return jsonify(result=None)
    
    # Make sure templates are available
    templatePath = '/opt/webapp/webrob/templates/package'
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
        app.logger.error("Unable to create package.")
        app.logger.error(str(sys.exc_info()[0]))
        app.logger.error(str(traceback.format_exc()))
        pkg_del(packageName)
    
    return jsonify(result=None)

@app.route('/pkg/del', methods=['POST'])
def pkg_del(packageName=None):
    pkgName = packageName
    if pkgName is None:
        pkgName = session['pkg']
    docker_interface.file_rm(session['user_container_name'], pkgName, True)
    return jsonify(result=None)

@app.route('/pkg/set', methods=['POST'])
def pkg_set():
    # Update package name
    data = json.loads(request.data)
    if 'packageName' in data and len(data['packageName'])>0:
        session['pkg'] = data['packageName']
    return get_pkg_tree()

@app.route('/pkg/list', methods=['POST'])
def pkg_list():
    # Return list of packages
    files = filter(lambda s: s['isdir'], docker_interface.file_ls(session['user_container_name'], '.')['children'])
    filenames = map(lambda s: s['name'], files)
    return jsonify(result=filenames)

@app.route('/pkg/read', methods=['POST'])
def pkg_read():
    path = get_file_path(json.loads(request.data)['file'])
    # Read the file
    content = docker_interface.file_read(session['user_container_name'], path).splitlines(True)
    return jsonify(result=content)

@app.route('/pkg/down', methods=['POST'])
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

@app.route('/pkg/save_exercise', methods=['POST'])
def pkg_save_exercise():
    db_adapter = current_app.user_manager.db_adapter
    # Query exercise DB object
    exercise_id = json.loads(request.data)['exercise_id']
    exercise = CourseExercise.query.filter_by(id=exercise_id).first()
    
    with LFTransfer(session['user_container_name']) as lft:
        # Create archive file
        name    = exercise.title
        zipName = name + '.zip'
        lft.from_container(session['pkg'], name) # rename package to match exercise name
        pkgPath = os.path.join(lft.get_filetransfer_folder(), name)
        zipPath = os.path.join(lft.get_filetransfer_folder(), zipName)
        zipf = zipfile.ZipFile(zipPath, 'w')
        zipdir(pkgPath, lft.get_filetransfer_folder(), zipf)
        zipf.close()
        # Read archive as binary blob and save in SQL DB
        zipfb = open(zipPath,'rb')
        # NOTE: need to convert to base64 so that jsonify does not complain
        exercise.archive = zipfb.read().encode('base64')
        db_adapter.commit()
        zipfb.close()
        # TODO: remove zip file
    
    return jsonify(result=None)

@app.route('/pkg/load_exercise', methods=['POST'])
def pkg_load_exercise():
    # Query exercise DB object
    exercise_id = json.loads(request.data)['exercise_id']
    exercise = CourseExercise.query.filter_by(id=exercise_id).first()
    pkgName = exercise.title
    zipName = pkgName + '.zip'
    
    if docker_interface.file_exists(session['user_container_name'], pkgName):
        app.logger.warning("Package already exists.") # TODO: notify client
        return jsonify(result=None)
    
    with LFTransfer(session['user_container_name']) as lft:
      # Create zip file
      zipPath = os.path.join(lft.get_filetransfer_folder(), zipName)
      zipfb = open(zipPath, 'wb')
      zipfb.write(exercise.archive.decode('base64'))
      zipfb.close()
      # unzip in intermediate container
      zipf = zipfile.ZipFile(zipPath, 'r')
      zipf.extractall(lft.get_filetransfer_folder())
      zipf.close()
      # copy to user container
      lft.to_container(pkgName, pkgName)
    
    return jsonify(result=None)

@app.route('/pkg/file_write', methods=['POST'])
def file_write():
    data = json.loads(request.data)
    path = get_file_path(data['file'])
    docker_interface.file_write(session['user_container_name'], data['content'], path)
    
    return jsonify(result=None)
   
@app.route('/pkg/file_del', methods=['POST'])
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
