
from flask import Flask, session, url_for, escape, request, render_template, g, abort, flash, Markup, send_from_directory, current_app, redirect
from flask_user import current_user, login_required
from flask.ext.misaka import markdown
from flask.ext.mail import Mail
from flask.ext.user import current_user, login_required, roles_required, SQLAlchemyAdapter, UserManager, UserMixin
from flask.ext.user.signals import user_logged_in
from flask.ext.user.signals import user_logged_out
from flask.ext.user.forms import RegisterForm

import os
import hashlib

import random
import string
import time
import re

from wtforms import validators
from wtforms import StringField
from wtforms import SelectField
from wtforms.validators import Required

from webrob.app_and_db import app, db
from webrob.docker import knowrob_docker
from webrob.user import knowrob_user

from urlparse import urlparse

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Web stuff

@user_logged_in.connect_via(app)
def track_login(sender, user, **extra):
    session['user_container_name'] = user.username
    session['user_data_container_name'] = user.username + "_data"
    session['common_data_container_name'] = "knowrob_data"
    session['rosauth_mac'] = generate_mac()
    session['show_loading_overlay'] = True
    knowrob_docker.start_container()
    #sender.logger.info('user logged in')

@user_logged_out.connect_via(app)
def track_logout(sender, user, **extra):
    knowrob_docker.stop_container()
    #sender.logger.info('user logged out')


@app.route('/')
def show_user_data():
    if not current_user.is_authenticated():
        return redirect(url_for('user.login'))
    #get_user_data(current_user.username)
    print request.host


    overlay = None
    if(session.get('show_loading_overlay') == True):
        overlay = True

        print "set overlay"
        session.pop('show_loading_overlay')

    return render_template('show_user_data.html', overlay=overlay)


#@app.route('/ws/<user_id>/')
#def ws_url(user_id=None):
  # dummy method to define endpoint; will be re-routed by reverse proxy
  # to the websockets endpoints
  #return




@app.route('/pr2_description/meshes/<path:filename>')
def download_mesh(filename):
  return send_from_directory('/opt/webapp/pr2_description/meshes/', filename, as_attachment=True)

@app.route('/knowrob_data/<path:filename>')
def download_logged_image(filename):
  return send_from_directory('/home/ros/knowrob_data/', filename)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != "" and request.form['password'] != ""):
            if is_valid_user(request.form['username'], request.form['password']):

                session['username'] = request.form['username']

                session['user_container_name'] = session['username']
                session['user_data_container_name'] = session['username'] + "_data"
                session['common_data_container_name'] = "knowrob_data"

                session['logged_in'] = True
                session['rosauth_mac'] = generate_mac()
                flash('You were logged in')

                session['show_loading_overlay'] = True

                knowrob_docker.start_container()
                return redirect(url_for('show_user_data'))
            else :
                error = 'Invalid user data'
    return render_template('login.html', error=error, action="login")

@app.route('/logout')
def logout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    session.pop('logged_in', None)
    knowrob_docker.stop_container()
    flash('You were logged out')
    return redirect(url_for('show_user_data'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':

        if (request.form['username'] == ""):
            error = 'Please specify a user name.'

        elif (request.form['password'] == ""):
            error = 'Please specify a password'

        elif(request.form['email'] == ""):
            error = 'Please specify an email address.'

        elif(user_exists(request.form['username'])):
            error = 'This username already exists. Please choose another username.'

        else:
            insert_user(request.form['username'], request.form['password'], request.form['email'])
            session['username'] = request.form['username']

            session['user_container_name'] = session['username']
            session['user_data_container_name'] = session['username'] + "_data"
            session['common_data_container_name'] = "knowrob_data"

            session['logged_in'] = True
            session['rosauth_mac'] = generate_mac()
            #create_data_containers()
            start_container()

            session['show_loading_overlay'] = True
            return redirect(url_for('show_user_data'))

    return render_template('login.html', error=error, action="register")



@app.route('/tutorials/')
@app.route('/tutorials/<cat_id>/')
@app.route('/tutorials/<cat_id>/<page>')
@login_required
def tutorials(cat_id='getting_started', page=1):

    #if not session.get('logged_in'):
    #    return redirect(url_for('login'))

    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = 'tutorials'

    tut = read_tutorial_page(cat_id, page)
    content = markdown(tut['text'], fenced_code=True)

    # automatically add "ask as query" links after code blocks
    content = re.sub('</code>(\s)?</pre>', "</code></pre><div class='show_code'><a href='#' class='show_code'>Ask as query</a></div>", str(content))
    content = Markup(content)

    # check whether there is another tutorial in this category
    nxt  = read_tutorial_page(cat_id, int(page)+1)
    prev = read_tutorial_page(cat_id, int(page)-1)

    return render_template('knowrob_tutorial.html', **locals())

@app.route('/knowrob')
@app.route('/exp/<exp_id>')
@login_required
def knowrob(exp_id=None):
    #if not session.get('logged_in'):
    #    return redirect(url_for('login'))
    error=""
    #current_app.logger.debug(request)
    # determine hostname/IP we are currently using
    # (needed for accessing container)
    host_url = urlparse(request.host_url).hostname
    container_name = session['user_container_name']

    if exp_id is not None and os.path.isfile('static/queries-' + exp_id + '.json'):
        exp_query_file='queries-' + exp_id + '.json'

    return render_template('knowrob_simple.html', **locals())



@app.route('/editor')
@app.route('/editor/<filename>/')
@login_required
def editor(filename=""):
    #if not session.get('logged_in'):
    #    return redirect(url_for('login'))

    error=""
    sandbox = '/home/tenorth/sandbox/'
    glob = sandbox + filename

    # check if still in sandbox
    if not str(os.path.abspath(glob)).startswith(sandbox):
        error = "Access denied to folders outside of sandbox"
        filename = ""

    files = os.listdir(glob)


    #poem = open("ad_lesbiam.txt").read()
    return render_template('editor.html', error=error, files=files)


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

