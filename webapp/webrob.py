from flask import Flask, session, redirect, url_for, escape, request, render_template, g, abort, flash, Markup
import sqlite3
import os
import hashlib
import docker
import markdown
import random
import string
import time
from docker.errors import *
from requests import ConnectionError


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'webrob.db'),
    DEBUG=True,
    SECRET_KEY='\\\xf8\x12\xdc\xf5\xb2W\xd4Lh\xf5\x1a\xbf"\x05@Bg\xdf\xeb>E\xd8<',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Docker stuff

def docker_connect():
    c = docker.Client(base_url='unix://var/run/docker.sock', version='1.12',timeout=10)
    return c
    

def create_data_containers():

    try:
        c = docker_connect()

        session['user_data_container_name'] = session['username'] + "_data"
        session['common_data_container_name'] = "knowrob_data"

        if(c is not None):
            c.create_container('knowrob/user_data', detach=True, tty=True, name=session['user_data_container_name'])

    except ConnectionError:
        flash("Error: Connection to your KnowRob instance failed.")
        return None


def start_container():

    try:
        c = docker_connect()

        if(c is not None):
            
            # check if container for this user still persists:

            found=False
            for cont in c.containers(all=True):
              if "/"+session['username'] in cont['Names']:
                found=True

            if not found:
                print('Creating container for ' + session['username'])
                c.create_container('knowrob/hydro-knowrob-daemon:1.0.1', detach=True, tty=True, name=session['username'])
                
            session['user_container_name'] = session['username']

            session['user_container_id'] = c.start(session['user_container_name'], publish_all_ports=True)
            session['port_1111'] = c.port(session['username'], 1111)[0]['HostPort']
            session['port_9090'] = c.port(session['username'], 9090)[0]['HostPort']

    except APIError, e:
        if "Conflict" in str(e.message):
            flash("Name conflict: Container for this user already exists")
        else:
            flash(e.message)
        return None
    except ConnectionError:
        flash("Error: Connection to your KnowRob instance failed.")
        return None


def stop_container():

    try:
        c = docker_connect()
        
        if(c is not None):
            print("Stopping container " + session['user_container_name'] + "...\n")
            c.stop(session['user_container_name'], timeout=5)

            print("Removing container " + session['user_container_name'] + "...\n")
            c.remove_container(session['user_container_name'])
            session.pop('user_container_name')

    except ConnectionError:
        flash("Error: Connection to your KnowRob instance failed.")
        return None


    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Web stuff

@app.route('/')
def show_user_data():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    get_user_data(session['username'])
    return render_template('show_user_data.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != "" and request.form['password'] != ""):
            if is_valid_user(request.form['username'], request.form['password']):
                session['username'] = request.form['username']
                session['logged_in'] = True
                session['rosauth_mac'] = generate_mac()
                flash('You were logged in')
                start_container()
                return redirect(url_for('show_user_data'))
            else :
                error = 'Invalid user data'
    return render_template('login.html', error=error, action="login")

@app.route('/logout')
def logout():
    stop_container()
    session.pop('logged_in', None)
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
            session['logged_in'] = True
            session['rosauth_mac'] = generate_mac()
	    create_data_containers()
            start_container()
            return redirect(url_for('show_user_data'))

    return render_template('login.html', error=error, action="register")



@app.route('/tutorials/')
@app.route('/tutorials/<cat_id>/')
@app.route('/tutorials/<cat_id>/<page>')
def tutorials(cat_id='basics', page=1):
  
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    tut = read_tutorial_page(cat_id, page)
    content = Markup(markdown.markdown(tut['text']))

    # check whether there is another tutorial in this category
    nxt  = read_tutorial_page(cat_id, int(page)+1)
    prev = read_tutorial_page(cat_id, int(page)-1)

    return render_template('knowrob_tutorial.html', **locals())

@app.route('/knowrob')
def knowrob():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    error=""
    return render_template('knowrob_simple.html', error=error)




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DB stuff

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context. """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def user_exists(username):
    db = get_db()
    cur = db.execute('select username from users where username=?', [username])
    entries = cur.fetchall()

    if len(entries)>0:
        return True
    else:
        return False


def is_valid_user(username, password):
    db = get_db()
    pwd_hash = hashlib.sha256(password).hexdigest()
    cur = db.execute('select username from users where username=? and passwd=?', [username, pwd_hash])
    entries = cur.fetchall()

    if len(entries)>0:
        return True
    else:
        return False


def insert_user(username, password, email):
    db = get_db()
    pwd_hash = hashlib.sha256(password).hexdigest()
    cur = db.execute('insert into users (username, passwd, email, container_id) values (?,?,?,"")', [username, pwd_hash, email])
    db.commit()
    flash('New user was successfully created')
    return redirect(url_for('show_user_data'))


def get_user_data(username):
    db = get_db()
    cur = db.execute('select * from users where username=?', [username])
    data = cur.fetchone()

    if data is not None:
        session['pwd_has'] = data['passwd']
        session['email'] = data['email']
        session['user_container_id'] = data['container_id']
        return data
    else:
        return False


def read_tutorial_page(cat, page):
    db = get_db()
    cur = db.execute('select * from tutorial where cat_id=? and page=?', [cat, page])
    tut = cur.fetchone()
    return tut


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
    


if __name__ == '__main__':
    app.run()