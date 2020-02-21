from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Process
from jobs.cron import facebook_job, twitter_job
from db import DB
from models.users import User
from middlewares.serializer import serialize

db_obj = DB() ### creating a object of DB function in db.py file
db_session = db_obj.get_db() ### getting a session of database

def facebook_job_trigger():
    try:
        print("Starting facebook job")

        user = serialize(db_session.query(User).all())
        if user is not None:
            for item in user['data']:
                facebook_job(item['email_id'])
        
        if user is None:
            pass
        
        print("Ran facebook job")
    
    except Exception as e: 
        print(e)

def twitter_job_trigger():
    try:
        print("Starting twitter job")

        user = serialize(db_session.query(User).all())
        if user is not None:
            for item in user['data']:
                twitter_job(item['email_id'])
        
        if user is None:
            pass
        
        print("Ran twitter job")
    
    except Exception as e: 
        print(e)

def scheduled_job():
    p1 = Process(target=facebook_job_trigger)
    p1.start()
    p2 = Process(target=twitter_job_trigger)
    p2.start()


'''def job_trigger():
    scheduled_job()'''

    
scheduler = BlockingScheduler()
scheduler.add_job(scheduled_job, 'interval', hours=1)
scheduler.start()
