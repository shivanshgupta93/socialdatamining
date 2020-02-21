BASE_URL = "https://dhcr.clarin-dariah.eu/api/v1/" ### Client data URL

EDUCATION = {
    "countries": "countries/index",
    "institutions": "institutions/index?sort_count"
} ### Parameters for client data URL


FB_CLIENT_ID = ''
FB_CLIENT_SECRET = ''

TW_API_KEY = ''
TW_API_SECRET = ''

graph_url = 'https://graph.facebook.com/'

facebook_url_feed = 'me?fields=id,feed.include_hidden(true).show_expired(true){story,created_time,status_type,message,caption,id,type,description,attachments{url,description,title,type}}'

twitter_url_feed = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'
