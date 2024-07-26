'''
Contains configuration settings for the Flask application, including the secret key for session management,
the URI for the SQLite database, and SQLAlchemy settings. This file centralizes configuration parameters
to maintain separation of concerns and facilitate easier updates.
'''

class Config:
    SECRET_KEY = '12345'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
