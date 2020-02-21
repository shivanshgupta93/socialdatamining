import os
import requests
from requests_oauthlib import OAuth1Session
import datetime
from consts import *
from db import DB
from models.users import User
from models.facebook import Facebook
from models.twitter import Twitter
from objects.twitter_object import twitter_auth
from middlewares.deserializer import deserializer, binary_to_json

db_obj = DB() ### creating a object of DB function in db.py file
db_session = db_obj.get_db() ### getting a session of database

def facebook_job(email_id):
    user = db_session.query(User).filter(User.email_id == email_id).first()
    
    facebook_data = binary_to_json(requests.get(graph_url + facebook_url_feed, params={'access_token':user.fb_access_token}))
    fb_id = facebook_data['id']

    for item in facebook_data['feed']['data']:
        facebook_return = db_session.query(Facebook).filter(Facebook.id == item['id'].split('_')[1]).first()
        
        if facebook_return is None:
            id = item['id'].split('_')[1]
            status_type = item.get('status_type',None)
            caption=item.get('caption',None) 
            story=item.get('story',None)
            message=item.get('message',None)
            description=item.get('description',None)
            fb_type=item.get('type',None)
            created_time=item['created_time']

            if 'attachments' in item:
                for attach in item['attachments']['data']:

                    db_session.add_all(
                                        [
                                            Facebook(id=id, fb_id=fb_id, status_type=status_type, caption=caption, story=story,
                                                message=message, description=description, type=fb_type, 
                                                attach_url=attach.get('url',None),
                                                attach_title=attach.get('title',None), 
                                                attach_type=attach.get('type',None),
                                                attach_description=attach.get('description',None),
                                                created_time=created_time)
                                        ]
                                )
            if 'attachments' not in item:
                db_session.add_all([
                                    Facebook(id=id, fb_id=fb_id, status_type=status_type, caption=caption, story=story,
                                    message=message, description=description, type=fb_type, created_time=created_time)
                                        ])

            db_session.commit()

        if facebook_return is not None:
            pass

def twitter_job(email_id):
    user = db_session.query(User).filter(User.email_id == email_id).first()

    oauth = OAuth1Session(TW_API_KEY,
                       client_secret=TW_API_SECRET,
                       resource_owner_key=user.tw_access_token,
                       resource_owner_secret=user.tw_access_token_secret)

    twitter_data = binary_to_json(oauth.get(twitter_url_feed, params={'usernames':user.tw_id}))
    
    for item in twitter_data:

        twitter_return = db_session.query(Twitter).filter(Twitter.id == str(item['id'])).first()

        if twitter_return is None:
            urls_list = item['entities']['urls']
            if len(urls_list) == 0:
                url = None
            
            if len(urls_list) != 0:
                url = urls_list[0].get('url', None)

            tw_created_time = str(datetime.datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S +%f %Y').strftime('%Y-%m-%d %H:%M:%S'))
            db_session.add_all([
                Twitter(id=item['id'], tw_id=item['user']['screen_name'], text=item['text'], retweet_count=int(item['retweet_count']),
                        retweeted=str(item['retweeted']), reply_user=item['in_reply_to_screen_name'], 
                        url=url, created_time=tw_created_time)
            ])
            db_session.commit()

        if twitter_return is not None:
            pass


def facebook_user(email_id, id, name, access_token):
    user = db_session.query(User).filter(User.email_id == email_id).first()
    if user is None:
        db_session.add_all(
                    [User(email_id=email_id, fb_id=id, fb_name=name, fb_access_token=access_token)]
                    )
    
    if user is not None:
        db_session.query(User).filter(User.email_id == email_id).update({User.fb_id:id, User.fb_name:name, User.fb_access_token:access_token,
        User.inserted_date: datetime.datetime.now().date()}, synchronize_session = False)
    
    db_session.commit()

def twitter_user(email_id, id, name, access_token, access_token_secret):
    user = db_session.query(User).filter(User.email_id == email_id).first()
    if user is None:
        db_session.add_all(
                    [User(email_id=email_id, tw_id=id, tw_name=name, tw_access_token=access_token, tw_access_token_secret=access_token_secret)]
                    )
    
    if user is not None:
        db_session.query(User).filter(User.email_id == email_id).update({User.tw_id:id, User.tw_name:name, User.tw_access_token:access_token,
        User.tw_access_token_secret: access_token_secret,
        User.inserted_date: datetime.datetime.now().date()}, synchronize_session = False)
    
    db_session.commit()
