
from flask import session, request, redirect, url_for
from flask_oauth import OAuth
from flask_login import login_user

from webrob.app_and_db import app, db
from webrob.models.users import User

from webrob.startup.init_app import add_user

oauth = OAuth()

GITHUB_APP_ID = 'da3ba583bc1a3de8b12d'
GITHUB_APP_SECRET = 'db37c38d09e0f43da8139d96a8b185a5681e7a02'

FACEBOOK_APP_ID = '1614655168857888'
FACEBOOK_APP_SECRET = '669369048a6d5cfb13c28ea58977e8e1'

TWITTER_APP_ID = 'CpiU3g4u0ZBsKqkc0a6LpFX7H'
TWITTER_APP_SECRET = 'Jwv797wfGu4eDEeQmI6pA6S3ET30bGh8ALrhFmMcfRvsJCNOnk'

GITHUB_APP_ID = 'da3ba583bc1a3de8b12d'
GITHUB_APP_SECRET = 'Jwv797wfGu4eDEeQmI6pA6S3ET30bGh8ALrhFmMcfRvsJCNOnk'

#GOOGLE_APP_ID = '1092402106799-q512i745g1163ibcee9npnn6si3bn5nk.apps.googleusercontent.com'
GOOGLE_APP_ID = '1092402106799-asoo7defvibhapnlmutimgbc8tkh7r3o.apps.googleusercontent.com'
#GOOGLE_APP_SECRET = 'Wpa7hN2VOQu1RNM2AcVUcPbJ'
GOOGLE_APP_SECRET = 'HlsdG6ItJ7wMydWOnkJHdUB9'

github = oauth.remote_app('github',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=GITHUB_APP_ID,
    consumer_secret=GITHUB_APP_SECRET
)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=TWITTER_APP_ID,
    consumer_secret=TWITTER_APP_SECRET
)

google = oauth.remote_app('google',
    base_url='https://www.google.com/accounts/',
    request_token_url=None,
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email', 'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    consumer_key=GOOGLE_APP_ID,
    consumer_secret=GOOGLE_APP_SECRET)

@github.tokengetter
@facebook.tokengetter
@twitter.tokengetter
@google.tokengetter
def get_outh_token():
    return session.get('oauth_token')

@app.route("/facebook/login")
def facebook_login():
    if session.has_key('oauth_token'): del session['oauth_token']
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next'), _external=True))

@app.route('/twitter/login')
def twitter_login():
    if session.has_key('oauth_token'): del session['oauth_token']
    return twitter.authorize(callback=url_for('twitter_authorized',
      next=request.args.get('next') or request.referrer or None))

@app.route('/google/login')
def google_login():
    if session.has_key('oauth_token'): del session['oauth_token']
    return twitter.authorize(callback=url_for('google_authorized',
      next=request.args.get('next') or request.referrer or None))

@app.route('/github/login')
def google_login():
    if session.has_key('oauth_token'): del session['oauth_token']
    return twitter.authorize(callback=url_for('github_authorized',
      next=request.args.get('next') or request.referrer or None))

@app.route("/github_authorized")
@github.authorized_handler
def github_authorized(resp):
    console.info('github_authorized');
    console.info(str(dir(resp)));
    
    next_url = request.args.get('next') or '/'
    if resp is None or 'oauth_token' not in resp:
        return redirect(next_url)
    
    session['oauth_token'] = (resp['access_token'], '')
    session['logged_in'] = True
    session['user_container_name'] = resp['screen_name']
    session['username'] = resp['screen_name']
    
    login_user(add_user(app, db, app.user_manager,
        resp['screen_name'],
        resp['screen_name']+'@github.com',
        resp['oauth_token'], []
    ))
    
    return redirect(next_url)

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or '/'
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)
    
    session['oauth_token'] = (resp['access_token'], '')
    session['logged_in'] = True
    
    me = facebook.get('/me')
    session['user_container_name'] = me.data['id']
    session['username'] = me.data['id']
    
    login_user(add_user(app, db, app.user_manager,
        me.data['id'],
        me.data['name']+'@facebook.com',
        resp['access_token'], []
    ))

    return redirect(next_url)

@app.route("/twitter_authorized")
@twitter.authorized_handler
def twitter_authorized(resp):
    next_url = request.args.get('next') or '/'
    if resp is None or 'oauth_token' not in resp:
        return redirect(next_url)
    
    session['oauth_token'] = (resp['oauth_token'], '')
    session['logged_in'] = True
    session['user_container_name'] = resp['screen_name']
    session['username'] = resp['screen_name']
    
    login_user(add_user(app, db, app.user_manager,
        resp['screen_name'],
        resp['screen_name']+'@twitter.com',
        resp['oauth_token'], []
    ))
    
    return redirect(next_url)

@app.route("/google_authorized")
@google.authorized_handler
def google_authorized(resp):
    console.info('google_authorized');
    console.info(str(dir(resp)));
    
    next_url = request.args.get('next') or '/'
    if resp is None or 'oauth_token' not in resp:
        return redirect(next_url)
    
    session['oauth_token'] = (resp['access_token'], '')
    session['logged_in'] = True
    session['user_container_name'] = resp['screen_name']
    session['username'] = resp['screen_name']
    
    login_user(add_user(app, db, app.user_manager,
        resp['screen_name'],
        resp['screen_name']+'@google.com',
        resp['oauth_token'], []
    ))
    
    return redirect(next_url)

