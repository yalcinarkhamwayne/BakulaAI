from app import db  # db wird hier importiert, weil es nun initialisiert ist

class Protocol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chiffre = db.Column(db.String(100), nullable=False)
    stimmung = db.Column(db.Integer, nullable=False)
    bemerkungen = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='protocols')
