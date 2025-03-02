from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Initialisierung von SQLAlchemy
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        print(self.password_hash)
        return check_password_hash(self.password_hash, password)

class Protocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chiffre = db.Column(db.String(100), nullable=False)
    stimmung = db.Column(db.Integer, nullable=False)
    bemerkungen = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('protocols', lazy=True))
