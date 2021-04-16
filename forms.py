from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TransactionForm(FlaskForm):
    #email = StringField('Email',
    #                    validators=[DataRequired(), Email()])
    PriKey = FileField('P/O Private Key', validators=[FileAllowed(['pdf', 'txt'])])
    PubKey = FileField('DO Public key', validators=[FileAllowed(['pdf', 'txt'])])
    file =  FileField('File', validators=[FileAllowed(['pdf', 'txt'])])
    submit = SubmitField('Send')