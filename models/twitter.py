from sqlalchemy import Column, Integer, String, Date
from models.base import Base
import datetime

#### User class to create User table
class Twitter(Base):
    __tablename__ = 'twitter'

    id = Column(String, primary_key=True)
    tw_id = Column(String)
    text = Column(String)
    retweet_count = Column(Integer)
    retweeted = Column(String)
    reply_user = Column(String)
    url = Column(String)
    created_time = Column(String)
    inserted_date = Column(Date(), default=datetime.datetime.now().date())

    def __repr__(self):
        return "<Twitter (id='%s', tw_id='%s', text='%s', retweet_count='%d', retweeted='%s', reply_user='%s', url='%s', created_time='%s', inserted_date='%s' )" % (self.id, self.tw_id, self.text, self.retweet_count, self.retweeted, self.reply_user, self.url, self.created_time, self.inserted_date)
