#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# @author Daniel Beßler

from flask import session, render_template
from flask_user import login_required

from webrob.app_and_db import app
from webrob.docker import docker_interface

@app.route('/log')
@login_required
def log():
    logStr = docker_interface.get_container_log(session['user_container_name'])
    return render_template('log.html', log=logStr)
