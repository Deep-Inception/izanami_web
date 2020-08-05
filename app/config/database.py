from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import current_app
from flask.cli import with_appcontext
import os
import sys
sys.path.append('../')

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8&auth_plugin_map={auth_plugin_map}'.format(**{
      'user': 'root',
      'password': 'izaname_web',
      'host': 'izanami-mysql',
      'db_name': 'db_izanami',
      'auth_plugin_map' : {'mysql_native_password'}
    })
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    from models import model, race, timetable_racer, racer_result, result, racer_pred_dl
    Base.metadata.create_all(bind=engine)