class Config:
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': 'izanami',
      'password': 'izaname_web',
      'host': 'izanami-mysql',
      'db_name': 'db_izanami'
    })
  DEBUG = False
  TESTING = False

class ProductionConfig(Config):
  DEBUG = False
  TESTING = False

class DevelopmentConfig(Config):
  DEBUG = True
