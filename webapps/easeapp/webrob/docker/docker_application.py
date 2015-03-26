from flask import session

from webrob.pages.utility import get_application_description
from webrob.docker import docker_interface

def ensure_application_started():
    application_name = session['application_name']
    if application_name is None: return False
    
    if not docker_interface.container_exists(session['user_container_name'], application_name):
        return start_application()
    else:
        return True

def start_application():
    application_name = session['application_name']
    if application_name is None: return
    
    application_description = get_application_description(application_name)
    if application_description is None: return
    
    docker_interface.start_user_container(
        session['user_container_name'], 
        session['user_home_dir'],
        application_description['application'],
        application_description['application_links'],
        application_description['application_volumes'])
    
    return True
