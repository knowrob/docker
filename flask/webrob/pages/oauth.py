"""
Sign in using external app such as github, twitter, ...
"""

from flask import session, request, redirect, url_for
from flask_oauth import OAuth
from flask_login import login_user

from sqlalchemy.exc import IntegrityError

import requests
from json import loads

from webrob.app_and_db import app, db
from webrob.models.users import User
from webrob.startup.init_app import add_user
from webrob.config.settings import FACEBOOK_APP_TOKENS, TWITTER_APP_TOKENS, GITHUB_APP_TOKENS, GOOGLE_APP_TOKENS

__author__ = 'danielb@cs.uni-bremen.de'

GOOGLE_OAUTH_USERINFO = 'https://www.googleapis.com/oauth2/v1/userinfo'

oauth = OAuth()

def tokens_defined(tokens):
    (tok0,tok1) = tokens
    return len(tok0)>0 and len(tok1)>0

github = oauth.remote_app('github',
    base_url='https://api.github.com/',
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    request_token_url=None,
    request_token_params=None,
    consumer_key=GITHUB_APP_TOKENS[0],
    consumer_secret=GITHUB_APP_TOKENS[1]
) if tokens_defined(GITHUB_APP_TOKENS) else None

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_TOKENS[0],
    consumer_secret=FACEBOOK_APP_TOKENS[1],
    request_token_params={'scope': 'email'}
) if tokens_defined(FACEBOOK_APP_TOKENS) else None

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=TWITTER_APP_TOKENS[0],
    consumer_secret=TWITTER_APP_TOKENS[1]
) if tokens_defined(TWITTER_APP_TOKENS) else None

google = oauth.remote_app('google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email', 'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=GOOGLE_APP_TOKENS[0],
    consumer_secret=GOOGLE_APP_TOKENS[1]
) if tokens_defined(GOOGLE_APP_TOKENS) else None

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
    (name,mail,pw) = get_user_information(response)
    session['user_container_name'] = name
    session['username'] = name
    
    try:
        flask_user = add_user(app, db, app.user_manager, name, mail, pw, [])
        if not app.user_manager.verify_password(pw,flask_user):
            # Username is taken, unable to sign in
            # TODO: do something here: tell the user at least
            app.logger.warn('Remote app password not matching.')
            return redirect('/')
        login_user(flask_user)
        return redirect(request.args.get('next') or '/')
    except IntegrityError, e:
        # Mail is taken, unable to sign in
        # TODO: do something here: tell the user at least
        app.logger.warn('Duplicate key violates unique key restriction. ')
        app.logger.warn(str(e))
        return redirect('/')

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
        github_user = github.get('/user').data
        user_name = github_user['login']
        return (get_user_name(user_name),
                get_user_mail(user_name, 'github.com'),
                response['access_token'])
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
        facebook_user = facebook.get('/me').data
        user_name = facebook_user['name']
        # NOTE: The access_token changes with each call and thus can not be used as password
        return (get_user_name(user_name),
                get_user_mail(user_name, 'facebook.com'),
                facebook_user['id'])
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
                get_user_mail(response['screen_name'], 'twitter.com'),
                response['oauth_token_secret'])
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
                get_user_mail(data['name'], 'google.com'),
                response['id_token'])
    try:
        return remote_app_authorized(response, 'access_token', user_information)
    except KeyError, e:
        app.logger.warn('google user information incomplete. ')
        app.logger.warn(str(e))
    except requests.HTTPError, e:
        app.logger.warn('Google user information request failed. ')
        app.logger.warn(str(e))
    return redirect('/')
