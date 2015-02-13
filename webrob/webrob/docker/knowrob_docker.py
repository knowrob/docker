import os.path
from urllib2 import URLError
import pyjsonrpc

from flask import flash
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


def start_container(user_container_name, user_data_container_name, common_data_container_name, user_home_dir):
    try:
        c = docker_connect()

        if c is not None:
            c.notify("start_container", user_container_name,user_data_container_name,
                     common_data_container_name)
            # create home directory if it does not exist yet
            if not os.path.exists(user_home_dir):
                os.makedirs(user_home_dir)

    except InternalError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def stop_container(user_container_name):
    try:
        c = docker_connect()
        if c is not None:
            c.notify("stop_container", user_container_name)

    except InternalError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def get_container_ip(user_container_name):
    try:
        c = docker_connect()
        if c is not None:
            return c.get_container_ip(user_container_name)
    except InternalError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def get_container_log(user_container_name):
    try:
        c = docker_connect()
        if c is not None:
            return c.get_container_log(user_container_name)
    except InternalError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your KnowRob instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")