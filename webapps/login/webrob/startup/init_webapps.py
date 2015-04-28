
from webrob.docker import docker_interface

def init_webapps(app):
    # Start all web applications
    for webapp_container in docker_interface.get_webapp_image_names():
        docker_interface.start_webapp_container(webapp_container)
