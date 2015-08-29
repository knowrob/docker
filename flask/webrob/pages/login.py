
from flask import session, request, redirect, url_for, render_template, jsonify
from flask.ext.user.signals import user_logged_in
from flask.ext.user.signals import user_logged_out
from flask_user import current_user
from flask_user import current_app
from flask_user import login_required

from urlparse import urlparse

from webrob.app_and_db import app
from webrob.docker import docker_interface

@user_logged_in.connect_via(app)
def track_login(sender, user, **extra):
    app.logger.info("Logged in " + str(user.username))
    session['user_container_name'] = user.username
    session['username'] = user.username
    session['api_token'] = user.api_token
    session['application_name'] = 'knowrob/hydro-knowrob-daemon'

@user_logged_out.connect_via(app)
def track_logout(sender, user, **extra):
    if 'user_container_name' in session:
        docker_interface.stop_container(session['user_container_name'])
        session.pop('user_container_name')

@app.route('/application_names', methods=['POST'])
def application_names():
    application_name = ''
    if 'application_name' in session:
        application_name = session['application_name']
    
    return jsonify(result=docker_interface.get_application_image_names(), selection=application_name)

@app.route('/application/<path:application_name>')
@login_required
def select_application(application_name):
    # TODO: I don't think that's needed in compination with login_required decorator
    if not current_user.is_authenticated():
        return redirect(url_for('user.login'))
    session['application_name'] = application_name
    return redirect('/'+application_name)

@app.route('/')
def show_user_data():
    if not current_user.is_authenticated():
        return redirect(url_for('user.login'))
    if not 'user_container_name' in session:
        return redirect(url_for('user.logout'))
    
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']
    application_names = docker_interface.get_application_image_names()
    role_names = map(lambda x: str(x.name), current_user.roles)

    return render_template('show_user_data.html', **locals())
