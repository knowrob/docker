
import os
import sys
import traceback

from flask import send_from_directory
from flask_user import login_required
from urllib import urlopen, urlretrieve
from subprocess import call

from webrob.app_and_db import app
from webrob.config.settings import MESH_REPOSITORIES

__author__ = 'danielb@cs.uni-bremen.de'

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
def download_mesh(mesh):
    meshFile = os.path.join('/home/ros/mesh_data', mesh)
    if not os.path.isfile(meshFile):
        for repository in MESH_REPOSITORIES:
            sourceFile = repository + mesh
            try:
                if download_mesh_to_local_cache(sourceFile, meshFile):
                    break
            except:
                app.logger.error(str(sys.exc_info()[0]))
                app.logger.error(str(traceback.format_exc()))
                pass
    
    return send_from_directory(
        os.path.dirname(meshFile),
        os.path.basename(meshFile))
