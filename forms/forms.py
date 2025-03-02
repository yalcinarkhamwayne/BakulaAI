from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms import SubmitField

# Login-Formular
class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Anmelden')

# Registrierung-Formular
class RegisterForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired(), Length(min=3, max=100)])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField('Registrieren')

# Protokoll-Formular
class ProtocolForm(FlaskForm):
    chiffre = StringField('Chiffre', validators=[DataRequired(), Length(min=1, max=100)])
    stimmung = IntegerField('Stimmung (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    bemerkungen = TextAreaField('Bemerkungen', validators=[Length(max=500)])
    submit = SubmitField('Protokoll speichern')
