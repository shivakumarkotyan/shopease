import os

class Config:
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password'  # Change to your MySQL password
    MYSQL_DB = 'shopease'
    MYSQL_CURSORCLASS = 'DictCursor'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False