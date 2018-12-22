import os
import sys


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
WIN = sys.platform.startswith('win')
prefix = 'sqlite:///' if WIN else 'sqlite:////'


class BaseConfig:
    SITE_NAME = 'URL猎手'
    GITHUB_USERNAME = 'alphardex'
    EMAIL = '2582347430@qq.com'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'f43hrt53et53'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    URL_PER_PAGE = 50
    URL_LIMIT = 10000
    SEARCH_PER_PAGE = URL_PER_PAGE
    REGEX_PER_PAGE = 10


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
