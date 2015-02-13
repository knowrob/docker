
from flask import session, request, redirect, url_for, render_template
from urlparse import urlparse
from flask.ext.user.signals import user_logged_in
from flask.ext.user.signals import user_logged_out
from flask_user import current_user

from webrob.app_and_db import app
from webrob.docker import knowrob_docker

@user_logged_in.connect_via(app)
def track_login(sender, user, **extra):
    session['user_container_name'] = user.username
    session['username'] = user.username
    session['user_data_container_name'] = "user_data"
    session['common_data_container_name'] = "knowrob_data"
    session['exp'] = None
    session['user_home_dir'] = '/home/ros/user_data/' + session['user_container_name']
    session['show_loading_overlay'] = True
    session['api_token'] = user.api_token
    if not 'pkg' in session: session['pkg'] = ''
    
    knowrob_docker.start_container(session['user_container_name'], session['user_data_container_name'],
                                   session['common_data_container_name'],session['user_home_dir'])
    session['container_ip'] = knowrob_docker.get_container_ip(session['user_container_name'])
    #sender.logger.info('user logged in')

@user_logged_out.connect_via(app)
def track_logout(sender, user, **extra):
    knowrob_docker.stop_container(session['user_container_name'])
    session.pop('user_container_name')
    #sender.logger.info('user logged out')

@app.route('/')
def show_user_data():
    if not current_user.is_authenticated():
        return redirect(url_for('user.login'))
    
    error=""
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']

    return render_template('show_user_data.html', **locals())