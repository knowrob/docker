import os.path
from urllib2 import URLError
import pyjsonrpc

from flask import session, flash
from pyjsonrpc.rpcerror import InternalError
from webrob.app_and_db import app


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Docker stuff

def docker_connect():
    http_client = pyjsonrpc.HttpClient(
        url="http://"+os.environ['DOCKERBRIDGE_PORT_5001_TCP_ADDR'] + ':'
            + os.environ['DOCKERBRIDGE_PORT_5001_TCP_PORT']
    )
    return http_client


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

        if c is not None:
            c.notify("start_container", session['user_container_name'], session['user_data_container_name'],
                     session['common_data_container_name'])
            # create home directory if it does not exist yet
            if not os.path.exists(session['user_home_dir']):
                os.makedirs(session['user_home_dir'])

    except InternalError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def stop_container():

    try:
        c = docker_connect()
        if c is not None:
            c.notify("stop_container", session['user_container_name'])
            session.pop('user_container_name')

    except InternalError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")
