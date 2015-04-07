
from webrob.docker import docker_interface
from webrob.pages.utility import get_application_description, get_applications

def register_routes():
    from webrob.pages import log
    from webrob.pages import meshes
    from webrob.pages import login
    from webrob.pages import api
    
    # Start all web applications
    for app in get_applications():
        desc = get_application_description(app)
        docker_interface.start_webapp_container(app, desc['webapp'],
            desc['webapp_links'], desc['webapp_volumes'])
