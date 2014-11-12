import docker
import os.path

from docker.errors import *

from flask import Flask, session, url_for, escape, request
from requests import ConnectionError
from flask_user import current_user, login_required


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Docker stuff

def docker_connect():
    c = docker.Client(base_url='unix://var/run/docker.sock', version='1.12',timeout=10)
    return c


#def create_data_containers():

    #try:
        #c = docker_connect()

        #session['user_data_container_name'] = session['username'] + "_data"
        #session['common_data_container_name'] = "knowrob_data"

        #if(c is not None):
            #c.create_container('knowrob/user_data', detach=True, tty=True, name=session['user_data_container_name'])

    #except ConnectionError:
        #flash("Error: Connection to your KnowRob instance failed.")
        #return None


def start_container():

    try:
        c = docker_connect()

        if(c is not None):

            all_containers = c.containers(all=True)

            # check if containers exist:
            user_cont_exists=False
            user_data_cont_exists=False
            common_data_exists=False
            mongo_cont_exists=False

            for cont in all_containers:
              if "/"+session['user_container_name'] in cont['Names']:
                user_cont_exists=True
              if "/"+session['user_data_container_name'] in cont['Names']:
                user_data_cont_exists=True
              if "/"+session['common_data_container_name'] in cont['Names']:
                common_data_exists=True
              if "/mongo_db" in cont['Names']:
                mongo_cont_exists=True


            # Create containers if they do not exist yet
            if not user_cont_exists:
                print('Creating container for ' + current_user.username)
                c.create_container('knowrob/hydro-knowrob-daemon',
                                    detach=True,
                                    tty=True,
                                    environment={"VIRTUAL_HOST" : session['user_container_name'], "VIRTUAL_PORT" : "9090"}, # for nginx reverse proxy
                                    name=session['user_container_name'])

            if not user_data_cont_exists:
                c.create_container('knowrob/user_data', detach=True, tty=True, name=session['user_data_container_name'], entrypoint='true')
                c.start(session['user_data_container_name'])

            if not common_data_exists:
                c.create_container('knowrob/knowrob_data', detach=True, name=session['common_data_container_name'], entrypoint='true')
                c.start(name=session['common_data_container_name'])

            if not mongo_cont_exists:
                c.create_container('busybox', detach=True, name='mongo_data', volumes=['/data/db'], entrypoint='true')
                c.create_container('mongo',   detach=True,ports=[27017], name='mongo_db')
                c.start('mongo', port_bindings={27017:27017}, volumes_from=['mongo_data'])

            current_user.container_id = c.start(session['user_container_name'],
                                                   publish_all_ports=True,
                                                   links={('mongo_db', 'mongo')},
                                                   volumes_from=[session['user_data_container_name'],
                                                                 session['common_data_container_name']])

            # create home directory if it does not exist yet
            if not os.path.exists(session['user_home_dir']):
                os.makedirs(session['user_home_dir'])
           

    except APIError, e:
        if "Conflict" in str(e.message):
            flash("Name conflict: Container for this user already exists")
        else:
            flash(e.message)
        return None
    except ConnectionError:
        flash("Error: Connection to your KnowRob instance failed.")
        return None


def stop_container():

    try:
        c = docker_connect()

        if(c is not None):
            all_containers = c.containers(all=True)

            # check if containers exist:
            user_cont_exists=False

            for cont in all_containers:
                if "/"+session['user_container_name'] in cont['Names']:
                    user_cont_exists=True

            if user_cont_exists:

                print("Stopping container " + session['user_container_name'] + "...\n")
                c.stop(session['user_container_name'], timeout=5)

                print("Removing container " + session['user_container_name'] + "...\n")
                c.remove_container(session['user_container_name'])


            session.pop('user_container_name')

    except ConnectionError:
        flash("Error: Connection to your KnowRob instance failed.")
        return None

