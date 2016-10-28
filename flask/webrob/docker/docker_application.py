from flask import session

from webrob.docker import docker_interface


def ensure_application_started(application_container):
    session['application_container'] = application_container
    if not 'user_container_name' in session: return False
    
    if not docker_interface.container_started(session['user_container_name']):
        return start_application()
    else:
        return True


def start_application():
    if not 'application_container' in session: return False
    if not 'user_container_name' in session: return False
    application_container = session['application_container']
    
    docker_interface.start_user_container(application_container, session['user_container_name'])
    
    return True