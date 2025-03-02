from flask_login import UserMixin
from datetime import datetime
from app import db

# Protokoll-Klasse
class Protocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chiffre = db.Column(db.String(100), nullable=False)
    stimmung = db.Column(db.Integer, nullable=False)
    bemerkungen = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Protocol {self.id}>"