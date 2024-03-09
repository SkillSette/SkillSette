import os


class Config(object):
    DEBUG = False
    TESTING = False
    MONGO_URI = os.environ.get('MONGO_URI')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
