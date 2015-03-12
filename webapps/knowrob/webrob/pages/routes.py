
from flask import session

from webrob.pages.utility import get_application_description
from webrob.docker import knowrob_docker

def ensure_knowrob_started():
    if not knowrob_docker.container_exists(session['user_container_name']):
        # TODO: validate that it's really a knowrob container
        start_knowrob()
    return True

def start_knowrob():
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

def register_routes():
    from webrob.pages import log
    from webrob.pages import meshes
    from webrob.pages import editor
    from webrob.pages import views
