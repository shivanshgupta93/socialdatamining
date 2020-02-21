from consts import TW_API_KEY, TW_API_SECRET
from rauth.service import OAuth1Service

twitter_auth = OAuth1Service(name='twitter',
                            consumer_key=TW_API_KEY,
                            consumer_secret=TW_API_SECRET,
                            request_token_url='https://api.twitter.com/oauth/request_token',
                            authorize_url='https://api.twitter.com/oauth/authorize',
                            access_token_url='https://api.twitter.com/oauth/access_token',
                            base_url='https://api.twitter.com/1.1/')