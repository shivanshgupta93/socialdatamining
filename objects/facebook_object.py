from consts import graph_url, FB_CLIENT_ID, FB_CLIENT_SECRET
from rauth.service import OAuth2Service

facebook_auth = OAuth2Service(name='facebook',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            access_token_url=graph_url + 'oauth/access_token',
                            client_id=FB_CLIENT_ID,
                            client_secret=FB_CLIENT_SECRET,
                            base_url=graph_url)