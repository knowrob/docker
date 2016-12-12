import base64
import hashlib
import os
import shutil
from urllib2 import URLError
import pyjsonrpc

from flask import flash, session
from pyjsonrpc.rpcerror import JsonRpcError
from webrob.app_and_db import app
from webrob.utility import random_string


client = pyjsonrpc.HttpClient(url="http://"+os.environ['DOCKERBRIDGE_PORT_5001_TCP_ADDR'] + ':'
                              + os.environ['DOCKERBRIDGE_PORT_5001_TCP_PORT'])


def generate_mac(user_container_name, client_name, dest, rand, t, level, end, cache=False):
    """
    Generate the mac for use with rosauth. Choose params according to rosauth specification.
    """
    if cache and 'secret_t' in session and session['secret_t'] > t:
        secret = session['secret_key']
    else:
        secret = client.files_readsecret(user_container_name)
        if cache:
            session['secret_t'] = t + 60
            session['secret_key'] = secret
    return hashlib.sha512(secret + client_name + dest + rand + str(t) + level + str(end)).hexdigest()


def clear_secretcache():
    if 'secret_t' in session:
        del session['secret_t']
    if 'secret_key' in session:
        del session['secret_key']


def get_application_image_names():
    try:
        return client.get_application_image_names()
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")
    return None


def get_webapp_image_names():
    try:
        return client.get_webapp_image_names()
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")
    return None


def start_user_container(application_image, user_container_name, ros_distribution):
    """
    Starts a user container based on the given image. If the container already exists, it will stop and remove the
    container first. Also, a data container is created and mounted inside the given container, and a rosauth secret
    is generated.

    Note that containers are stopped and removed after 10 minutes if the refresh function is not called periodically
    beforehand.
    
    :param application_image: Image the container should be based on
    :param user_container_name: Name of the container.
    """
    try:
        client.notify("create_user_data_container", user_container_name)
        client.notify("files_writesecret", user_container_name, random_string(16))
        clear_secretcache()
        client.notify("start_user_container", application_image, user_container_name, ros_distribution)
    except JsonRpcError, e:
        flash("Error: Connection to your OpenEASE instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your OpenEASE instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def start_webapp_container(webapp_image):
    """
    Starts a new web container based on the given image. If it already exists, no action will be taken.
    :param webapp_image: Image the container should be based on
    """
    try:
        client.notify("start_webapp_container", webapp_image)
    except JsonRpcError, e:
        flash("Error: Connection to your OpenEASE instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your OpenEASE instance failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def stop_container(user_container_name):
    """
    Stops and deletes a user container.
    :param user_container_name: Name of the container.
    """
    try:
        client.notify("stop_container", user_container_name)
        clear_secretcache()
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def container_started(user_container_name, base_image=None):
    """
    Returns true if the container exists and is running. If a base_image is specified, it only return true if the
    container exists and is directly derived from the given base_image
    :param user_container_name: Name of the container.
    :param base_image: Image the container is based on
    """
    try:
        return client.container_started(user_container_name, base_image)
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")
    return None


def get_container_ip(user_container_name):
    """
    Returns the internal IP of the container.
    :param user_container_name: Name of the container.
    """
    try:
        return client.get_container_ip(user_container_name)
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")
    return None


def get_container_log(user_container_name):
    """
    Returns the stdout/stderr of the container.
    :param user_container_name: Name of the container.
    """
    try:
        return client.get_container_log(user_container_name)
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def get_container_env(user_container_name, key):
    try:
        return client.get_container_env(user_container_name, key)
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def refresh(user_container_name):
    """
    Resets the kill timeout for the given container. Containers are normally stopped and removed after 10 minutes of
    inactivity. Call this method on user activity to extend the timer back to 10 minutes.
    :param user_container_name: Name of the container.
    """
    try:
        client.notify("refresh", user_container_name)
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def file_exists(user_container_name, file):
    """
    Returns true if the given file exists in the data container associated to the given container.
    :param user_container_name: Name of the container.
    :param file: relative filename. The service automatically adds /home/ros/user_data. Non relative filenames and
    parent directory declarations (../) are forbidden and will not work.
    """
    try:
        return client.files_exists(user_container_name, file)
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def file_rm(user_container_name, file, recursive=False):
    """
    Deletes the given file in the data container associated to the given container.
    :param user_container_name: Name of the container.
    :param file: relative filename. The service automatically adds /home/ros/user_data. Non relative filenames and
    parent directory declarations (../) are forbidden and will not work.
    :param recursive: True if deletion should be done recursively (e.g. for directories)
    """
    try:
        client.notify("files_rm", user_container_name, file, recursive)
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def file_ls(user_container_name, dir, recursive=False):
    """
    Returns a listing of the given directory in the data container associated to the given container.
    It will return a dictionary of the type { "name": directory_name, "isdir": True, "children": [...] }, with the
    children being a list of all the files inside the directory. They have the same dictionary structure as the root
    element.
    :param user_container_name: Name of the container.
    :param dir: relative directory path. The service automatically adds /home/ros/user_data. Non relative pathes and
    parent directory declarations (../) are forbidden and will not work.
    :param recursive: True if subdirectories should also be listed
    """
    try:
        return client.files_ls(user_container_name, dir, recursive)
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def file_read(user_container_name, file):
    """
    Returns the content of the given file in the data container associated to the given container as string.
    :param user_container_name: Name of the container.
    :param file: relative file path. The service automatically adds /home/ros/user_data. Non relative pathes and
    parent directory declarations (../) are forbidden and will not work.
    """
    try:
        return base64.b64decode(client.files_fromcontainer(user_container_name, file))
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


def file_write(user_container_name, data, file):
    """
    Write the content of data to the given file in the data container associated to the given container.
    :param user_container_name: Name of the container.
    :param data: data to write to the file
    :param file: relative file path. The service automatically adds /home/ros/user_data. Non relative pathes and
    parent directory declarations (../) are forbidden and will not work.
    """
    try:
        client.notify("files_tocontainer", user_container_name, base64.b64encode(data), file)
    except JsonRpcError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e.message) + str(e.data) + "\n")
    except URLError, e:
        flash("Error: Connection to your application failed.")
        app.logger.error("ConnectionError during connect: " + str(e) + "\n")


class LFTransfer(object):
    """
    This class can be used in a with statement ( with LFTransfer() as lft: ) to copy large files/directories from/to
    the data container associated to the given container. The lft_data data container needs to be mounted inside the
    executing container beforehand. On initialization, a directory is created inside the lft_data container, where
    files can be placed for copying, or files can be copied to from the users data container. After the with-block ends,
    the directory inside the lft_data container is automatically removed.

    Example for copying data to the users container:
        with LFTransfer('user123') as lft:
            filename = os.path.join(lft.get_filetransfer_folder(), "large.file")
            f = open(filename, 'w')
            f.write("test")
            f.close()
            lft.to_container(filename, filename)

    Example for copying data from the users container:
        content = ''
        with LFTransfer('user123') as lft:
            filename = "my_experiment/owl/test.owl"
            lft.to_container(filename, filename)
            lft_path = os.path.join(lft.get_filetransfer_folder(), filename)
            f = open(lft_path, 'w')
            content = f.read()
            f.close()
    """
    def __init__(self, user_container):
        self.lftdir = None
        self.user_container = user_container

    def get_filetransfer_folder(self):
        return self.lftdir

    def to_container(self, sourcefile, targetfile):
        if '/tmp/openEASE/dockerbridge' in sourcefile:
            source = os.path.relpath(sourcefile, '/tmp/openEASE/dockerbridge')
        elif self.lftdir not in sourcefile:
            source = os.path.relpath(os.path.join(self.lftdir, sourcefile), '/tmp/openEASE/dockerbridge')
        else:
            source = sourcefile
        client.notify("files_largetocontainer", self.user_container, source, targetfile)

    def from_container(self, sourcefile, targetfile):
        if '/tmp/openEASE/dockerbridge' in targetfile:
            target = os.path.relpath(targetfile, '/tmp/openEASE/dockerbridge')
        elif self.lftdir not in targetfile:
            target = os.path.relpath(os.path.join(self.lftdir, targetfile), '/tmp/openEASE/dockerbridge')
        else:
            target = targetfile
        client.notify("files_largefromcontainer", self.user_container, sourcefile, target)

    def __enter__(self):
        if not os.access('/tmp/openEASE/dockerbridge/', os.W_OK):
            client.notify("files_lft_set_writeable")
        self.lftdir = os.path.join('/tmp/openEASE/dockerbridge', random_string(16))
        os.mkdir(self.lftdir)
        return self

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self.lftdir, True)