#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# @author Daniel Beßler

import os, random, string, time, hashlib

from flask import session, request

def get_user_dir():
    userDir = "/home/ros/user_data/" + session['user_container_name']
    if not os.path.exists(userDir):
        print("Creating user directory at " + userDir)
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
 
def generate_mac():
    secret = "RW6WZ2yp67ETMdj2"
    client = request.remote_addr
    dest   = request.host_url # TODO: find out the actual IP; this will return the hostname

    rand = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(30)])

    t = int(time.time())
    level = "user"
    end = int(t + 3600)

    mac = hashlib.sha512(secret + client + dest + rand + str(t) + level + str(end) ).hexdigest()

    return "ros.authenticate(" + mac + ", " + client + ", " + dest + ", " + rand + ", " + str(t) + ", " + level + ", " + str(end) + ")"
 