import docker
import os.path
import traceback
import pyjsonrpc
from docker.errors import *

from flask import Flask, session, url_for, escape, request, flash
from requests import ConnectionError
from flask_user import current_user, login_required
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
        app.logger.info("Connecting to docker...")
        c = docker_connect()
        app.logger.info("Connected to docker.")

        if c is not None:
            start_container.start_container(session['user_container_name'],
                                            session['user_data_container_name'],
                                            session['common_data_container_name'])

    except ConnectionError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect:" + str(e.message) + "\n")
        traceback.print_exc()
        return None

def stop_container():

    try:
        c = docker_connect()
        if c is not None:
            start_container.stop_container(session['user_container_name'])

    except ConnectionError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during disconnect:" + str(e.message) + "\n")
        traceback.print_exc()
        return None

