import os

EXPIRED_TIME = os.getenv('EXPIRED_TIME', 3600)
SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
