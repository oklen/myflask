import os


basedir = os.path.abspath(os.path.dirname(__name__))
DEBUG = True
HOST = '127.0.0.1'
PORT = '3306'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI =\
                          "{db}://{user}:{password}@{addr}/{uri}".\
                          format(db='mysql',
                                 user='root',
                                 password='$pythonandmysql960719first',
                                 addr=HOST,
                                 uri='flask')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,
                                       'db_repositiory')
