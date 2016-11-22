
import os
import sys
import traceback

from flask import send_from_directory, jsonify
from flask_user import login_required
from urllib import urlopen, urlretrieve
from subprocess import call
from posixpath import basename
import thread

from webrob.app_and_db import app
from webrob.config.settings import MESH_REPOSITORIES

__author__ = 'danielb@cs.uni-bremen.de'

def is_mesh_url_valid(url):
    return urlopen(url).getcode() == 200

def update_meshes_run():
    os.chdir('/home/ros/mesh_data')
    # FIXME: make this threaded because it blocks flask
    #  also it takes long time when no internet connection is available
    for (tool,url) in MESH_REPOSITORIES:
        if tool=="svn":
            update_meshes_svn(url)
        elif tool=="git":
            update_meshes_git(url)
    # Convert tif images to png images
    call(['/opt/webapp/convert-recursive', '/home/ros/mesh_data'])

def update_meshes():
    thread.start_new_thread(update_meshes_run, ())

def update_meshes_svn(url):
    repo_name = basename(url)
    if os.path.exists(repo_name):
      os.chdir(repo_name)
      call(["/usr/bin/svn","update"])
      os.chdir('..')
    else:
      call(["/usr/bin/svn","co",url])

def update_meshes_git(url):
    repo_name = basename(url)
    if os.path.exists(repo_name):
      os.chdir(repo_name)
      call(["/usr/bin/git","pull"])
      os.chdir('..')
    else:
      call(["/usr/bin/git","clone",url])


@app.route('/meshes/<path:mesh>')
def download_mesh(mesh):
    meshFile = None
    for repo in os.listdir( '/home/ros/mesh_data' ):
        repoPath = os.path.join('/home/ros/mesh_data', repo)
        meshPath = os.path.join(repoPath, mesh)
        if os.path.exists(meshPath):
            meshFile = meshPath
    
    if meshFile == None:
        if os.path.exists(mesh): meshFile = mesh
        elif os.path.exists('/'+mesh): meshFile = '/'+mesh
    
    if meshFile == None:
        app.logger.info("Unable to download mesh " + mesh)
        return jsonify(result=None)
    
    return send_from_directory(
        os.path.dirname(meshFile),
        os.path.basename(meshFile))
