from sqlalchemy import Column, Integer, String, Date
from models.base import Base
import datetime

#### User class to create User table
class Facebook(Base):
    __tablename__ = 'facebook'

    id = Column(String, primary_key=True)
    fb_id = Column(String)
    status_type = Column(String)
    caption = Column(String)
    story = Column(String)
    message = Column(String)
    description = Column(String)
    type = Column(String)
    attach_url = Column(String)
    attach_title = Column(String)
    attach_type = Column(String)
    attach_description = Column(String)
    created_time = Column(String)
    inserted_date = Column(Date(), default=datetime.datetime.now().date())

    def __repr__(self):
        return "<Facebook (id='%s', fb_id='%s', status_type='%s', caption='%s', story='%s', message='%s', description='%s', type='%s', attach_url='%s', attach_title='%s', attach_type='%s', attach_description='%s', created_time='%s', inserted_date='%s' )" % (self.id, self.fb_id, self.status_type, self.caption, self.story, self.message, self.description, self.type, self.attach_url, self.attach_title, self.attach_type, self.attach_description, self.created_time, self.inserted_date)
