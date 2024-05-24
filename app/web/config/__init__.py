import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SESSION_PERMANENT = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']
    MAILGUN_DOMAIN = os.environ['MAILGUN_DOMAIN']
    MAILGUN_DEFAULT_SENDER = os.environ['MAILGUN_DEFAULT_SENDER']
    FRONTEND_URL = os.environ['FRONTEND_URL']
