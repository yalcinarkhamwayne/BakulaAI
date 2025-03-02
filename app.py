from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from models import db, User, Protocol
from forms import LoginForm, RegisterForm, ProtocolForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("Ungültiger Benutzername oder Passwort")
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

 