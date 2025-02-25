from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Protocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Da "Chiffre" ausschließlich Zahlen enthalten soll, könnte man hier auch Integer verwenden.
    # Bei Bedarf, z.B. wegen führender Nullen, kann man String verwenden.
    chiffre = db.Column(db.String(20), nullable=False)
    stimmung = db.Column(db.Integer, nullable=False)
    bemerkungen = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  