
from flask import session, request, redirect, url_for, render_template
from flask.ext.user.signals import user_logged_in
from flask.ext.user.signals import user_logged_out
from flask_user import current_user

from urlparse import urlparse

from webrob.app_and_db import app
from webrob.docker import docker_interface

@user_logged_in.connect_via(app)
def track_login(sender, user, **extra):
    app.logger.info("Logged in " + str(user.username))
    session['user_container_name'] = user.username
    session['username'] = user.username
    session['api_token'] = user.api_token

@user_logged_out.connect_via(app)
def track_logout(sender, user, **extra):
    if 'user_container_name' in session:
        docker_interface.stop_container(session['user_container_name'])
        session.pop('user_container_name')

@app.route('/')
def show_user_data():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    if not 'user_container_name' in session:
        return redirect(url_for('user.logout'))
    
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']
    role_names = map(lambda x: str(x.name), current_user.roles)
    
    category = None
    exp = None
    if 'exp-category' in session: category = session['exp-category']
    if 'exp-name' in session: exp = session['exp-name']
    
    return render_template('main.html', **locals())
    #return render_template('show_user_data.html', **locals())
