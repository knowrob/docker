
import os

from flask import send_from_directory
from flask_user import login_required
from urllib import urlopen, urlretrieve
from webrob.app_and_db import app
from subprocess import call

__author__ = 'danielb@cs.uni-bremen.de'

MESH_REPOSITORIES = [
    "http://svn.ai.uni-bremen.de/svn/cad_models/",
    "https://github.com/code-iai/iai_maps/raw/master/",
    "https://github.com/bbrieber/iai_robots/raw/master/",
    "https://github.com/PR2/pr2_common/raw/master/"
    #"https://github.com/code-iai/iai_robots/raw/master/",
    #"https://code.ros.org/svn/wg-ros-pkg/stacks/pr2_common/trunk/"
]

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
        for repository in MESH_REPOSITORIES:
            sourceFile = repository + mesh
            try:
                if download_mesh_to_local_cache(sourceFile, meshFile):
                    break
            except:
                pass
    
    return send_from_directory(
        os.path.dirname(meshFile),
        os.path.basename(meshFile))
