import secret, os

class Config:
    MYSQL_HOST = secret.DATABASE_SERVER
    MYSQL_PORT = secret.DATABASE_PORT
    MYSQL_USER = secret.DATABASE_USER
    MYSQL_PASSWORD = secret.DATABASE_PASSWORD
    MYSQL_DB = secret.DATABASE_NAME
    MYSQL_CURSORCLASS = "DictCursor"

    TESTING = True
    
    SECRET_KEY = os.urandom(16)