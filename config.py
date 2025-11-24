import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'hansini'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'vitatracker'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
