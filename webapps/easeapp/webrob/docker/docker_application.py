from flask import session

from webrob.docker import docker_interface


def ensure_application_started(application_container):
    session['application_container'] = application_container
    
    if not docker_interface.container_started(session['user_container_name']):
        return start_application()
    else:
        return True


def start_application():
    application_container = session['application_container']
    if application_container is None: return
    
    docker_interface.start_user_container(application_container, session['user_container_name'])
    
    return True