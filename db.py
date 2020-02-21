from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from models.base import Base
import os


class DB:
    __session = None

    def __init__(self): ### constructor of DB class
        if not DB.__session:
            DB.__session = self.create_db_session()

    def create_db_session(self):
        env = os.environ.get("env", "development") ### setting environment by default as development
        engine = None
        if env == "development":
            engine = create_engine("sqlite:///social_data.db", echo = True, connect_args={'check_same_thread': False}) ## creating sqlite db
            Base.metadata.create_all(engine) ### creating database and tables if it does not exists

        elif env == "production":
            db_uri = os.environ.get("DATABASE_URL", "") ## getting production database url from environment variables
            engine = create_engine(db_uri, pool_pre_ping=True, pool_size=2) #postgres
            Base.metadata.create_all(engine) ### creating database and tables if it does not exists
        else:
            raise Exception("environment not available")

        Session = sessionmaker(bind = engine)
        session = Session() ### creating a session of the database

        return session

    def get_db(self):
        return DB.__session

    def close(self):
        DB.__session.close()