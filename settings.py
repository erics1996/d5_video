
class Config(object):
    SECRET_KEY = '0160a068dba74c5aa21f5b93cc6b95c5'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/d5_video?charset=utf8mb4'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
