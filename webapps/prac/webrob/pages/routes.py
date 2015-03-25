from flask import session
from webrob.pages.utility import get_application_description
from webrob.docker import knowrob_docker

from prac.wordnet import WordNet
from webrob.app_and_db import app
from webrob.pracinit import prac

import os


def init(prac):
    # initialize folder for fileupload
    app.config['UPLOAD_FOLDER'] = session['user_home_dir'] + '/pracfiles/'
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'])):
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER']))
    app.config['ALLOWED_EXTENSIONS'] = set(['mln','db','pracmln'])

    # initialize WordNet
    prac.wordnet = WordNet(concepts=None)


def ensure_prac_started():
    if not knowrob_docker.container_exists(session['user_container_name']):
        # TODO: validate that it's really a knowrob container
        start_prac()
    return True


def start_prac():
    application_name = session['application_name']
    if application_name is None: return
    
    application_description = get_application_description(application_name)
    if application_description is None: return
    
    knowrob_docker.start_user_container(
        session['user_container_name'],
        session['user_home_dir'],
        application_description['application'],
        application_description['application_links'],
        application_description['application_volumes'])
    
    init(prac)


def register_routes():
    from webrob.pages import log
    from webrob.pages import meshes
    from webrob.pages import views

