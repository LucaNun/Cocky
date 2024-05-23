import secret, os

class Config:
    MYSQL_HOST = secret.DATABASE_HOST
    MYSQL_PORT = secret.DATABASE_PORT
    MYSQL_USER = secret.DaTABASE_USER
    MYSQL_PASSWORD = secret.DATABASE_PASSWORD
    MYSQL_DB = secret.DATABASE_NAME

    TESTING = True
    
    SECRET_KEY = os.urandom(16)