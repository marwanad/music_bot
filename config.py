import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'w44xM94T2y'
    SQL_ALCHEMY_COMMIT_ON_TEARDOWN = True
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHMEY_DATABASE_URI = 'postgres://' + os.environ.get('SONGIQ_DB_ADMIN') + ':' 
    os.environ.get('SONGIQ_DB_PASS') + '@' + os.environ.get('SONGIQ_DB_HOST')
    SQL_ALCHEMY_COMMIT_ON_TEARDOWN = True

class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
