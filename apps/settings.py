"""
settings.py

Configuration for Flask app

"""


class Config(object):
    # Set secret key to use session
    SECRET_KEY = "likelion-flaskr-secret-key"
    debug = False


class Production(Config):
    debug = True
    CSRF_ENABLED = False
    ADMIN = "gamiduka@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///TEST?instance=tra-la:example'
    migration_directory = 'migrations'

