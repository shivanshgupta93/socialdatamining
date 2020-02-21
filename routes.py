import datetime
import requests
from flask import Blueprint, request, flash, request, redirect, render_template, url_for, session
from db import DB
from models.users import User
from models.facebook import Facebook
from models.twitter import Twitter
from middlewares.serializer import serialize
from middlewares.deserializer import binary_to_json
from jobs.cron import facebook_user, twitter_user
from consts import graph_url, FB_CLIENT_ID, FB_CLIENT_SECRET
from rauth.utils import parse_utf8_qsl
from objects.facebook_object import facebook_auth
from objects.twitter_object import twitter_auth

db_obj = DB() ### creating a object of DB function in db.py file
db_session = db_obj.get_db() ### getting a session of database

facebook_api = Blueprint("facebook", __name__, url_prefix="/facebook")
twitter_api = Blueprint("twitter", __name__, url_prefix='/twitter')
api = Blueprint("api", __name__, url_prefix='/api')

@facebook_api.route('/login')
def login():
    redirect_uri = url_for('facebook.authorized', _external=True)
    params = {'redirect_uri': redirect_uri, 'scope':'email'}
    print(params)
    return redirect(facebook_auth.get_authorize_url(**params))

@facebook_api.route('/authorized')
def authorized():
    # check to make sure the user authorized the request
    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('index'))

    url = "https://graph.facebook.com/v6.0/oauth/access_token"

    params = {
    'client_id': FB_CLIENT_ID,
    'redirect_uri': url_for('facebook.authorized', _external=True),
    'client_secret': FB_CLIENT_SECRET,
    'code': request.args['code']
    }

    response = requests.get(url, params)
    access_data = binary_to_json(response)

    fb_access_token = access_data['access_token']
    user_response = requests.get(graph_url+'/me?fields=id,name,email', params={'access_token': fb_access_token})
    user_data = binary_to_json(user_response)

    facebook_user(user_data['email'], user_data['id'], user_data['name'], fb_access_token)
    
    return redirect('/static/facebook.html')

@twitter_api.route('/login')
def login():
    oauth_callback = url_for('twitter.authorized', _external=True)
    params = {'oauth_callback': oauth_callback}

    r = twitter_auth.get_raw_request_token(params=params)
    data = parse_utf8_qsl(r.content)

    session['twitter_oauth'] = (data['oauth_token'],data['oauth_token_secret'])
    return redirect(twitter_auth.get_authorize_url(data['oauth_token'], **params))

@twitter_api.route('/authorized')
def authorized():
    # check to make sure the user authorized the request
    print(request.args)
    request_token, request_token_secret = session.pop('twitter_oauth')
    if not 'oauth_token' in request.args:
        flash('You did not authorize the request')
        return redirect('/')

    creds = {'request_token': request_token, 'request_token_secret': request_token_secret}
    params = {'oauth_verifier': request.args['oauth_verifier']}
    sess, tw_token = twitter_auth.get_auth_session(params=params, **creds)

    verify = sess.get('account/verify_credentials.json',params={'format':'json', 'include_email':'true'}).json()

    twitter_user(verify['email'], verify['screen_name'], verify['name'], tw_token[0], tw_token[1])
    
    return redirect('/static/twitter.html')

@api.route('/user')
def user():
    user = serialize(db_session.query(User).all())
    for item in user['data']:
        del item['fb_access_token']
        del item['tw_access_token']
        del item['tw_access_token_secret']
    return user

@api.route('/facebook/<facebook_id>')
def facebook_data(facebook_id):
    data_facebook = db_session.query(Facebook).filter(Facebook.fb_id == facebook_id).all()
    return serialize(data_facebook)

@api.route('/twitter/<twitter_id>')
def twitter_data(twitter_id):
    data_twitter = db_session.query(Twitter).filter(Twitter.tw_id == twitter_id).all()
    return serialize(data_twitter)

