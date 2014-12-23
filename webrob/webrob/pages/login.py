
from webrob.docker import knowrob_docker

from flask import session, request, flash, redirect, url_for, render_template
from flask.ext.user.signals import user_logged_in
from flask.ext.user.signals import user_logged_out
from flask_user import current_user

from webrob.app_and_db import app
from webrob.docker import knowrob_docker

from utility import generate_mac

@user_logged_in.connect_via(app)
def track_login(sender, user, **extra):
    session['user_container_name'] = user.username
    session['username'] = user.username
    session['user_data_container_name'] = "user_data"
    session['common_data_container_name'] = "knowrob_data"
    session['exp'] = None
    session['rosauth_mac'] = generate_mac()
    session['show_loading_overlay'] = True
    if not 'pkg' in session: session['pkg'] = ''
    
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
    
    overlay = None
    if(session.get('show_loading_overlay') == True):
        overlay = True
        session.pop('show_loading_overlay')

    return render_template('show_user_data.html', overlay=overlay)

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

#@app.route('/ws/<user_id>/')
#def ws_url(user_id=None):
  # dummy method to define endpoint; will be re-routed by reverse proxy
  # to the websockets endpoints
  #return
