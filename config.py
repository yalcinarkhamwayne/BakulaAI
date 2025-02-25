import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "bakulaai"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "mysql+pymysql://bakulaai:bakulaai@192.168.2.241/bakulaai"
    SQLALCHEMY_TRACK_MODIFICATIONS = False