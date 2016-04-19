"""
Sign in using external app such as github, twitter, ...
"""

from flask import session, request, redirect, url_for
from flask_oauth import OAuth
from flask_login import login_user

import requests
from json import loads

from webrob.app_and_db import app, db
from webrob.models.users import User

from webrob.startup.init_app import add_user

__author__ = 'danielb@cs.uni-bremen.de'

oauth = OAuth()

# TODO: reset secrets and read them from environment
FACEBOOK_APP_ID = '1614655168857888'
FACEBOOK_APP_SECRET = '669369048a6d5cfb13c28ea58977e8e1'
TWITTER_APP_ID = 'CpiU3g4u0ZBsKqkc0a6LpFX7H'
TWITTER_APP_SECRET = 'Jwv797wfGu4eDEeQmI6pA6S3ET30bGh8ALrhFmMcfRvsJCNOnk'
GOOGLE_APP_ID = '1092402106799-asoo7defvibhapnlmutimgbc8tkh7r3o.apps.googleusercontent.com'
GOOGLE_APP_SECRET = 'HlsdG6ItJ7wMydWOnkJHdUB9'
GOOGLE_OAUTH_USERINFO = 'https://www.googleapis.com/oauth2/v1/userinfo'
GITHUB_APP_ID = 'da3ba583bc1a3de8b12d'
GITHUB_APP_SECRET = 'db37c38d09e0f43da8139d96a8b185a5681e7a02'

github = oauth.remote_app('github',
    base_url='https://api.github.com/',
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    request_token_url=None,
    request_token_params=None,
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
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email', 'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=GOOGLE_APP_ID,
    consumer_secret=GOOGLE_APP_SECRET
)

def remote_app_login(remote_app, authorized):
    if session.has_key('oauth_token'): del session['oauth_token']
    return remote_app.authorize(callback=url_for(authorized, _external=True,
      next=request.args.get('next') or request.referrer or None))

def remote_app_authorized(response, oauth_token_key, get_user_information):
    if response is None:
        app.logger.warn('remote app authorization response missing.')
        return redirect('/')
    if 'error' in response:
        app.logger.warn('Remote app authentication error: %s.' % (response['error']))
        return redirect('/')
    if oauth_token_key not in response:
        app.logger.warn('%s key missing in response.' % (oauth_token_key))
        app.logger.warn(str(response.keys()))
        return redirect('/')
    session['oauth_token'] = (response[oauth_token_key], '')
    session['logged_in'] = True
    (name,mail) = get_user_information(response)
    session['user_container_name'] = name
    session['username'] = name
    # FIXME(daniel): Name or email could be used already. Ideas:
    #       - Offer to reset credentials for used mail
    #       - Show name/mail selection dialog
    flask_user = add_user(app, db, app.user_manager,
                          name, mail, response[oauth_token_key], [])
    login_user(flask_user)
    return redirect(request.args.get('next') or '/')

def get_user_name(login):
    return login.replace(' ', '').replace('@','_').replace('.', '_')

def get_user_mail(login, domain):
    if not '@' in login: return login+'@'+domain
    else: return login

@github.tokengetter
@facebook.tokengetter
@twitter.tokengetter
@google.tokengetter
def get_outh_token(): return session.get('oauth_token')

@app.route("/facebook/login")
def facebook_login(): return remote_app_login(facebook, 'facebook_authorized')
@app.route('/twitter/login')
def twitter_login(): return remote_app_login(twitter, 'twitter_authorized')
@app.route('/google/login')
def google_login(): return remote_app_login(google, 'google_authorized')
@app.route('/github/login')
def github_login(): return remote_app_login(github, 'github_authorized')

@app.route("/github_authorized")
@github.authorized_handler
def github_authorized(response):
    def user_information(response):
        user_name = github.get('/user').data['login']
        return (get_user_name(user_name, 'github.com'),
                get_user_mail(user_name, 'github.com'))
    try:
        return remote_app_authorized(response, 'access_token', user_information)
    except KeyError, e:
        app.logger.warn('github user information incomplete. ')
        app.logger.warn(str(e))
    return redirect('/')

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(response):
    def user_information(response):
        user_name = facebook.get('/me').data['name']
        return (get_user_name(user_name),
                get_user_mail(user_name, 'facebook.com'))
    try:
        return remote_app_authorized(response, 'access_token', user_information)
    except KeyError, e:
        app.logger.warn('facebook user information incomplete. ')
        app.logger.warn(str(e))
    return redirect('/')

@app.route("/twitter_authorized")
@twitter.authorized_handler
def twitter_authorized(response):
    def user_information(response):
        return (get_user_name(response['screen_name']),
                get_user_mail(response['screen_name'], 'twitter.com'))
    try:
        return remote_app_authorized(response, 'oauth_token', user_information)
    except KeyError, e:
        app.logger.warn('twitter user information incomplete. ')
        app.logger.warn(str(e))
    return redirect('/')

@app.route("/google_authorized")
@google.authorized_handler
def google_authorized(response):
    def user_information(response):
        r = requests.get(GOOGLE_OAUTH_USERINFO,
                        headers={'Authorization': 'OAuth ' + response['access_token']})
        if not r.ok:
            app.logger.warn('Google user information request failed.')
            return redirect(request.args.get('next') or '/')
        data = loads(r.text)
        return (get_user_name(data['name']),
                get_user_mail(data['name'], 'google.com'))
    try:
        return remote_app_authorized(response, 'access_token', user_information)
    except KeyError, e:
        app.logger.warn('google user information incomplete. ')
        app.logger.warn(str(e))
    except requests.HTTPError, e:
        app.logger.warn('Google user information request failed. ')
        app.logger.warn(str(e))
    return redirect('/')
