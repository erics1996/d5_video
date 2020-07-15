import redis


class BaseConfig(object):
    SECRET_KEY = '0160a068dba74c5aa21f5b93cc6b95c5'
    # SQLALCHEMY配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/d5_video?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 10  # 最多超出10个连接
    # Redis配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, password='foobared')
    import datetime
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=30)
    import os
    FACE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app/static/home/uploads/users/")
    # print(os.path.abspath(os.path.dirname(__file__)))#/media/thanlon/存储盘/项目实施/开发/Flask/d5_video


class ProductionConfig(BaseConfig):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    DEBUG = True
