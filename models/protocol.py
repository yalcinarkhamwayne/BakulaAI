from app import db  # Importiere db aus app.py

class Protocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chiffre = db.Column(db.String(50), nullable=False)
    stimmung = db.Column(db.Integer, nullable=False)
    bemerkungen = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('protocols', lazy=True))
