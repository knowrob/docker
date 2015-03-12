
from flask import session, request, redirect, url_for, render_template, jsonify
from urlparse import urlparse
from flask.ext.user.signals import user_logged_in
from flask.ext.user.signals import user_logged_out
from flask_user import current_user
from flask_user import login_required
import json
import sys
import time

from webrob.app_and_db import app
from webrob.docker import knowrob_docker
from webrob.pages.utility import get_application_description

@user_logged_in.connect_via(app)
def track_login(sender, user, **extra):
    session['user_container_name'] = user.username
    session['username'] = user.username
    session['user_home_dir'] = '/home/ros/user_data/' + session['user_container_name']
    session['api_token'] = user.api_token
    session['application_name'] = ''
    
    #session['exp'] = None
    #if not 'pkg' in session: session['pkg'] = ''
    #session['user_data_container_name'] = "user_data"
    #session['common_data_container_name'] = "knowrob_data"
    #knowrob_docker.start_container(session['user_container_name'], session['user_data_container_name'],
    #                               session['common_data_container_name'],session['user_home_dir'])
    #session['container_ip'] = knowrob_docker.get_container_ip(session['user_container_name'])
    #sender.logger.info('user logged in')

@user_logged_out.connect_via(app)
def track_logout(sender, user, **extra):
    knowrob_docker.stop_container(session['user_container_name'])
    session.pop('user_container_name')
    #sender.logger.info('user logged out')

@app.route('/application_description/<application_name>', methods=['POST'])
def application_description(application_name):
    return jsonify(result=get_application_description(application_name))

@app.route('/application_names', methods=['POST'])
def application_names():
    return jsonify(result=app.config['APPLICATIONS'].keys(), selection=session['application_name'])

@app.route('/application', methods=['POST'])
@login_required
def select_application():
    if not current_user.is_authenticated():
        return redirect(url_for('user.login'))
    
    application_name = json.loads(request.data)['application_name']
    if application_name is None: return
    
    application_description = get_application_description(application_name)
    if application_description is None: return
    
    session['application_name'] = application_name
    
    # Start required webapp if not allready running
    knowrob_docker.start_webapp_container(
        application_name,
        application_description['webapp'],
        application_description['webapp_links'],
        application_description['webapp_volumes'])
    # XXX: wait for flask
    time.sleep(2)
    
    return jsonify(result=None)

@app.route('/')
def show_user_data():
    if not current_user.is_authenticated():
        return redirect(url_for('user.login'))
    
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']
    application_names = app.config['APPLICATIONS'].keys()

    return render_template('show_user_data.html', **locals())