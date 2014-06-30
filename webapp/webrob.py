from flask import Flask, session, redirect, url_for, escape, request, render_template, g, abort, flash
import sqlite3
import os
import hashlib


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
        session['container_id'] = data['container_id']
        return data
    else:
        return False

        

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
                flash('You were logged in')
                return redirect(url_for('show_user_data'))
            else :
                error = 'Invalid user data'
    return render_template('login.html', error=error, action="login")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_user_data'))

@app.route('/launch')
def launch():
    error=""
    return render_template('start_container.html', error=error)
  

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
            
        else:
            insert_user(request.form['username'], request.form['password'], request.form['email'])
            session['username'] = request.form['username']
            session['logged_in'] = True
            return redirect(url_for('show_user_data'))
            
    return render_template('login.html', error=error, action="register")



##@app.route('/')
##def index():
    ##if 'username' in session:
        ##return 'Logged in as %s' % escape(session['username'])
    ##return 'You are not logged in'

##@app.route("/login/", methods=['GET', 'POST'])
##def login():
    ##if request.method == 'POST':
        ##session['username'] = request.form['username']
        ##return redirect(url_for('index'))
    ##return render_template('login.html', css_url = url_for('static', filename='screen.css'))


##@app.route('/logout')
##def logout():
    ### remove the username from the session if it's there
    ##session.pop('username', None)
    ##return redirect(url_for('index'))



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


if __name__ == '__main__':
    app.run()

