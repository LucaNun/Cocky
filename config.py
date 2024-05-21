import secret, os

class Config:
    DATABASE = ""
    SECRET_KEY = os.urandom(16)