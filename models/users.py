from sqlalchemy import Column, Integer, String, Date
from models.base import Base
import datetime

#### User class to create User table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email_id = Column(String, unique=True)
    fb_id = Column(String)
    fb_name = Column(String)
    fb_access_token = Column(String)
    tw_name = Column(String)
    tw_id = Column(String)
    tw_access_token = Column(String)
    tw_access_token_secret = Column(String)
    inserted_date = Column(Date(), default=datetime.datetime.now().date())

    def __repr__(self):
        return "<User (email_id='%s', fb_id='%s', fb_name='%s', fb_access_token='%s', tw_name='%s', tw_id='%s', tw_access_token='%s', tw_access_token_secret='%s', inserted_date='%s' )" % (self.email_id, self.fb_id, self.fb_name, self.fb_access_token, self.tw_name, self.tw_id, self.tw_access_token, self.tw_access_token_secret, self.inserted_date)
