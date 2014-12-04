#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# @author Daniel Beßler

from flask import session, render_template

from webrob.app_and_db import app
from webrob.docker import knowrob_docker

@app.route('/log')
def log():
  c = knowrob_docker.docker_connect()
  container_id = session['user_container_name']
  logger = c.logs(container_id, stdout=True, stderr=True, stream=False, timestamps=False)
  
  logStr = ""
  for c in logger: logStr += c
  
  return render_template('log.html', log=logStr)
