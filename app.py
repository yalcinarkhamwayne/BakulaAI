from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from forms.forms import LoginForm, RegisterForm, ProtocolForm
from werkzeug.security import generate_password_hash, check_password_hash

# Initialisiere die Flask-App
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Erstelle die Flask-App
    app = Flask(__name__)
    
    # Konfiguration aus der Config-Klasse laden
    app.config.from_object(Config)
    
    # Initialisiere SQLAlchemy und LoginManager mit der App
    db.init_app(app)
    login_manager.init_app(app)

    # Setze die Login-Route für nicht authentifizierte Benutzer
    login_manager.login_view = "login"  # Hier wird der Name der Login-Route festgelegt

    # Benutzer-Loader für Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User  # Importiere die User-Klasse nach der Initialisierung von db
        return User.query.get(int(user_id))

    # Importiere die Modelle nach der App-Initialisierung
    from models.user import User  # Importiere die User-Klasse
    from models.protocol import Protocol  # Importiere die Protocol-Klasse
    
    # Routen und Logik
    @app.route('/')
    def index():
        return redirect(url_for('dashboard'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            # Versuche, den Benutzer aus der Datenbank zu finden
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)  # Login des Benutzers
                flash("Erfolgreich eingeloggt", "success")
                return redirect(url_for('dashboard'))  # Weiterleitung zur Dashboard-Seite
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
        protocols = Protocol.query.order_by(Protocol.timestamp.desc()).all()
        return render_template('protocols_overview.html', protocols=protocols)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    return app

app = create_app()

# Flask-App erstellen und starten
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
