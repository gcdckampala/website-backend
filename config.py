import os, sys
from dotenv import load_dotenv


load_dotenv()


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    TESTDB_NAME = os.getenv('TESTDB_NAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    USER_EMAIL_SENDER_EMAIL = 'cedric@fox.com'


    @classmethod
    def generate_url(cls, *args):
        env, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME = args
        return (os.getenv(env).format(DB_USER, DB_PASSWORD,
                                      DB_HOST, DB_NAME)).strip('\"')

# "postgresql://localhost:@localhost/wb"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.generate_url(
        'DATABASE_URL_PROD', Config.DB_USER, Config.DB_PASSWORD,
        Config.DB_HOST, Config.DB_NAME)


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = Config.generate_url(
        'DATABASE_URL_DEV', Config.DB_USER,
        Config.DB_PASSWORD, Config.DB_HOST, Config.DB_NAME)


class TestingConfig(Config):
    TESTING = not Config.TESTING
    DEBUG = not Config.DEBUG
    SQLALCHEMY_DATABASE_URI = Config.generate_url(
        'DATABASE_URL_TEST', Config.DB_USER, Config.DB_PASSWORD,
        Config.DB_HOST, Config.TESTDB_NAME)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

AppConfig = TestingConfig if 'pytest' in sys.modules else config.get(
    os.getenv('FLASK_ENV'), 'development')