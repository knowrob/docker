
from flask import session, request, redirect, url_for, render_template, jsonify
from flask.ext.user.signals import user_logged_in
from flask.ext.user.signals import user_logged_out
from flask_user import current_user
from flask_user import login_required
import json
import sys
import time

from urllib import urlopen
import httplib
from urlparse import urlparse
import urllib2

from webrob.app_and_db import app
from webrob.docker import docker_interface
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
    #docker_interface.start_container(session['user_container_name'], session['user_data_container_name'],
    #                               session['common_data_container_name'],session['user_home_dir'])
    #session['container_ip'] = docker_interface.get_container_ip(session['user_container_name'])
    #sender.logger.info('user logged in')

@user_logged_out.connect_via(app)
def track_logout(sender, user, **extra):
    if 'user_container_name' in session:
        docker_interface.stop_container(session['user_container_name'])
        session.pop('user_container_name')
        #sender.logger.info('user logged out')

@app.route('/application_description/<application_name>', methods=['POST'])
def application_description(application_name):
    return jsonify(result=get_application_description(application_name))

@app.route('/application_names', methods=['POST'])
def application_names():
    application_name = ''
    if 'application_name' in session:
        application_name = session['application_name']
    return jsonify(result=app.config['APPLICATIONS'].keys(), selection=application_name)

 
def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    # http://stackoverflow.com/questions/1140661
    host, path = urlparse(url)[1:3]    # elems [1] and [2]
    try:
        app.logger.error("get_server_status_code: " + str(url) + "\n")
        app.logger.error("host: " + str(host) + "\n")
        app.logger.error("path: " + str(path) + "\n")
        conn = httplib.HTTPConnection(host)
        conn.request('HEAD', path)
        app.logger.error(str(conn.getresponse().status) + "\n")
        return conn.getresponse().status
    except StandardError, e:
        app.logger.error("StandardError: " + str(e) + "\n")
        return None
 
def check_url(url):
    """
    Check if a URL exists without downloading the whole file.
    We only check the URL header.
    """
    # see also http://stackoverflow.com/questions/2924422
    good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
    return get_server_status_code(url) in good_codes

@app.route('/application/<application_name>')
@login_required
def select_application(application_name):
    if not current_user.is_authenticated():
        return redirect(url_for('user.login'))
    
    application_description = get_application_description(application_name)
    if application_description is None: return
    
    session['application_name'] = application_name
    
    # Start required webapp if not allready running
    #docker_interface.start_webapp_container(
    #    application_name,
    #    application_description['webapp'],
    #    application_description['webapp_links'],
    #    application_description['webapp_volumes'])
    
    # FIXME: This is bad. Nothing happens for n seconds and we can not be sure that
    # flask is ready to serve after this time.
    # - Show a spinner indicating the webapp startup in the browser
    # - Make sure that flask is ready to serve
    # time.sleep(3)
    #ip = docker_interface.get_container_ip(application_name)
    #app.logger.error("ip: " + str(ip) + "\n")
    #ip = 'localhost'
    #ip = '172.17.0.3'
    #ip = '172.17.42.1'
    #url = 'http://' + ip
    
    #while not check_url(url):
    #    time.sleep(1)
    
    #url = 'https://www.googleapis.com/language/translate/v2?'+query
    #response = urllib2.urlopen('http://python.org/')
    #html = response.read()
    #app.logger.error(html + '\n')
    #app.logger.error(str(response.code) + '\n')
    
    #url = 'http://' + ip + ':5000/'+application_name+'/menu'
    #while True:
    #    try:
    #        app.logger.error("urlopen: " + str(url) + "\n")
    #        response = urllib2.urlopen(url)
    #        app.logger.error("code: " + str(response.code) + "\n")
    #        if response.code == 200: break
    #    except IOError, e:
    #        app.logger.error("IOError: " + str(e) + "\n")
    #        pass
    #    time.sleep(1)
    
    # Wait for flask
    #x = None
    
    #for i in [1,2,3,4]:
    #    x = redirect('/'+application_name)
        
    #    app.logger.error("_: " + str(x) + "\n")
    #    app.logger.error("status: " + str(x.status) + "\n")
    #    app.logger.error("status_code: " + str(x.status_code) + "\n")
    #    app.logger.error("data: " + str(x.data) + "\n")
    #    app.logger.error("content_length: " + str(x.content_length) + "\n")
    #    app.logger.error("get_data: " + str(x.get_data()) + "\n")
    #    app.logger.error("get_wsgi_response: " + str(x.get_wsgi_response()) + "\n")
    #    app.logger.error("get_etag: " + str(x.get_etag()) + "\n")
    #    app.logger.error("__: " + str(dir(x)) + "\n")
    #    time.sleep(1)
    
    return redirect('/'+application_name)

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
