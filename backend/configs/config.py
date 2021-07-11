import os
class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8&auth_plugin_map={auth_plugin_map}'.format(**{
      'user': 'izanami',
      'password': 'izanami',
      'host': 'izanami-mysql',
      'db_name': 'db_izanami',
      'auth_plugin_map' : {'mysql_native_password'}
    })
    # cookieを暗号化する秘密鍵
    SECRET_KEY = os.urandom(24)
    # csrf token用秘密鍵
    WTF_CSRF_SECRET_KEY = os.urandom(24)

class ProductionConfig(BaseConfig):
    DEBUG = False
