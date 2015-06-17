
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# DB stuff

#def connect_db():
    #"""Connects to the specific database."""
    #rv = sqlite3.connect(app.config['DATABASE'])
    #rv.row_factory = sqlite3.Row
    #return rv

#def init_db():
    #with app.app_context():
        #db = get_db()
        #with app.open_resource('schema.sql', mode='r') as f:
            #db.cursor().executescript(f.read())
        #db.commit()


#def get_db():
    #"""Opens a new database connection if there is none yet for the
    #current application context. """
    #if not hasattr(g, 'sqlite_db'):
        #g.sqlite_db = connect_db()
    #return g.sqlite_db

#@app.teardown_appcontext
#def close_db(error):
    #"""Closes the database again at the end of the request."""
    #if hasattr(g, 'sqlite_db'):
        #g.sqlite_db.close()


#def user_exists(username):

    ## username blacklist
    #if username=="knowrob":
      #return True
    #elif username=="mongo":
      #return True
    #elif username=="tenorth":
      #return True


    #db = get_db()
    #cur = db.execute('select username from users where username=?', [username])
    #entries = cur.fetchall()

    #if len(entries)>0:
        #return True
    #else:
        #return False


#def is_valid_user(username, password):
    #db = get_db()
    #pwd_hash = hashlib.sha256(password).hexdigest()
    #cur = db.execute('select username from users where username=? and passwd=?', [username, pwd_hash])
    #entries = cur.fetchall()

    #if len(entries)>0:
        #return True
    #else:
        #return False


#def insert_user(username, password, email):
    #db = get_db()
    #pwd_hash = hashlib.sha256(password).hexdigest()
    #cur = db.execute('insert into users (username, passwd, email, container_id) values (?,?,?,"")', [username, pwd_hash, email])
    #db.commit()
    #flash('New user was successfully created')
    #return redirect(url_for('show_user_data'))


def get_user_data(username):
    #db = get_db()
    #cur = db.execute('select * from users where username=?', [username])
    #data = cur.fetchone()

    #if data is not None:
        #session['pwd_has'] = data['passwd']
        #session['email'] = data['email']
        #session['user_container_id'] = data['container_id']
        #return data
    #else:
        return False


#def read_tutorial_page(cat, page):
#    db = get_db()
#    cur = db.execute('select * from tutorial where cat_id=? and page=?', [cat, page])
#    tut = cur.fetchone()
#    return tut
 
