from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Regexp, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Passwort bestätigen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

class ProtocolForm(FlaskForm):
    chiffre = StringField('Chiffre', validators=[
        DataRequired(),
        Regexp('^[0-9]+$', message="Nur Zahlen erlaubt")
    ])
    stimmung = SelectField('Stimmung des Patienten',
                           choices=[(str(i), i) for i in range(1, 11)],
                           validators=[DataRequired()])
    bemerkungen = TextAreaField('Bemerkungen', validators=[Length(max=500)])
    submit = SubmitField('Speichern')
