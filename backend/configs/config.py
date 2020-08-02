import os
class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///backend.db'
    # cookieを暗号化する秘密鍵
    SECRET_KEY = os.urandom(24)
    # csrf token用秘密鍵
    WTF_CSRF_SECRET_KEY = os.urandom(24)