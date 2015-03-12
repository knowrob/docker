#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# @author Daniel Beßler

import os, random, string, time, hashlib

from flask import session, request
from webrob.app_and_db import app

def get_user_dir():
    userDir = "/home/ros/user_data/" + session['user_container_name']
    if not os.path.exists(userDir):
        app.logger.info("Creating user directory at " + userDir)
        os.makedirs(userDir)
    return userDir

def write_text_file(path, content):
    f = open(path, "w")
    f.write(content)
    f.close()

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