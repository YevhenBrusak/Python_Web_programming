from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm) :
    username = StringField("Username", validators=[DataRequired("Please enter your name."), Length(min=4, max=14, message ='Length of this field must be between 4 and 14'),
    Regexp(regex='^[A-Za-z][A-Za-z0-9_.]*$', message='Username must have only lettes, numbers, dots or underscores')])
    email = StringField('Email', validators=[DataRequired("Please enter your email."), Email("Please enter correct email")])
    password = PasswordField('Password', validators=[DataRequired("Please enter password"), Length(min=6, message="Length of this field must be min 6")])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired("Confirm your password"), EqualTo("password")])
    submit = SubmitField("Sign up")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

class LoginForm(FlaskForm) :
    email = StringField('Email', validators=[DataRequired("Please enter your email."), Email("Please enter correct email")])
    password = PasswordField('Password', [DataRequired("Please enter password")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
                       