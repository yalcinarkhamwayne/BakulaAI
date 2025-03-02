import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://bakulaai:bakulaai@192.168.2.20/bakulaai"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "zonguldak-Osch_§27012019")  # Falls Login-Session nötig
