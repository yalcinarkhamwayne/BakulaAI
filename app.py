from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from forms import LoginForm, RegisterForm, ProtocolForm
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Protocol  # Importiere db und Modelle aus models.py
from database import db


# Initialisiere SQLAlchemy und LoginManager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Konfiguration laden
    app.config.from_object(Config)

    # Initialisiere SQLAlchemy und LoginManager mit der App
    db.init_app(app)  # WICHTIG: db.init_app muss nach der App-Erstellung aufgerufen werden
    login_manager.init_app(app)

    # Setze die Login-Route für nicht authentifizierte Benutzer
    login_manager.login_view = "login" 
    
    # Benutzer-Loader für Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Routen und Logik
    @app.route('/')
    def index():
        return redirect(url_for('dashboard'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            print(f"Benutzername: {form.username.data}")
            user = User.query.filter_by(username=form.username.data).first()
            print(f"Gefundener Benutzer: {user}")
            if user and user.check_password(form.password.data):
                login_user(user) 
                flash("Erfolgreich eingeloggt", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Ungültiger Benutzername oder Passwort", "danger")
        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Registrierung erfolgreich. Bitte anmelden.")
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/protocols_overview')
    @login_required
    def protocols_overview():
        # Alle Chiffren mit den letzten Protokollen gruppiert nach Chiffre
        protocols = db.session.query(Protocol.chiffre, db.func.max(Protocol.timestamp).label('latest_timestamp')).group_by(Protocol.chiffre).all()
        return render_template('protocols_overview.html', protocols=protocols)
    
    @app.route('/protocols/<string:chiffre>')
    @login_required
    def protocols_by_chiffre(chiffre):
        protocols = Protocol.query.filter_by(chiffre=chiffre).order_by(Protocol.timestamp.desc()).all()
        return render_template('protocols_by_chiffre.html', protocols=protocols, chiffre=chiffre)


    @app.route('/protocol/new', methods=['GET', 'POST'])
    @login_required
    def new_protocol():
        form = ProtocolForm()
        if form.validate_on_submit():
            protocol = Protocol(
                chiffre=form.chiffre.data,
                stimmung=int(form.stimmung.data),
                bemerkungen=form.bemerkungen.data,
                user_id=current_user.id
            )
            db.session.add(protocol)
            db.session.commit()
            flash("Protokoll gespeichert")
            return redirect(url_for('dashboard'))
        return render_template('protocol_form.html', form=form)

    @app.route('/protocols')
    @login_required
    def protocols():
        query = Protocol.query

        # Filter nach Datum
        date = request.args.get("date")
        if date:
            query = query.filter(db.func.date(Protocol.timestamp) == date)

        # Filter nach Chiffre
        chiffre = request.args.get("chiffre")
        if chiffre:
            query = query.filter(Protocol.chiffre.like(f"%{chiffre}%"))

        # Filter nach Stimmung
        stimmung = request.args.get("stimmung")
        if stimmung:
            query = query.filter(Protocol.stimmung == int(stimmung))

        protocols = query.order_by(Protocol.timestamp.desc()).all()
        
        return render_template('protocols_overview.html', protocols=protocols)


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    return app

# Flask-App erstellen und starten
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
