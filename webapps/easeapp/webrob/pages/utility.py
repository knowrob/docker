#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# @author Daniel Beßler

import os
import string

from flask import session
from webrob.app_and_db import app
from Crypto.Random import random

def get_application_description(application_name):
    try:
        return app.config['APPLICATIONS'][application_name]
    except:
        return None

def get_applications():
    try:
        return app.config['APPLICATIONS'].keys()
    except:
        return None

def copy_template_file(src, dst, args):
    # Read the template file
    src_f = open(src, 'r')
    template = src_f.read()
    src_f.close()
    # Create the parent dir in user_data container
    parent = os.path.dirname(dst)
    if not os.path.exists(parent):  os.makedirs(parent)
    # Copy template to user directory while replacing some keywords
    dst_f = open(dst, 'w')
    dst_f.write(template % args)
    dst_f.close()


def get_user_dir():
    userDir = "/home/ros/user_data/" + session['user_container_name']
    if not os.path.exists(userDir):
        app.logger.info("Creating user directory at " + userDir)
        os.makedirs(userDir)
    return userDir


def random_string(length):
    return "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(length)])
