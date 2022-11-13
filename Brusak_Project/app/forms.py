from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError
from app.models import User

class Myform(FlaskForm):
    name = StringField("Name", 
                      [DataRequired("Please enter your name."), 
                       Length(min=4, max=10, message ='Length of this field must be between 4 and 10')
                       ]
                       )
    email = StringField('Email', validators=[DataRequired("Please enter your email."), Email("Please enter correct email")])
    phone = StringField('Phone',
    validators=[Regexp('(^\+380\s?[0-9]{2}\s?[0-9]{3}\s?[0-9]{4}$)$', message='Enter correct number')])
    subject = SelectField('Subject', choices=['Mathematics', 'Biology', 'Philosophy', 'English'])
    message = TextAreaField('Message', validators=[DataRequired("Please enter message."), Length(min=0,max=500, message ='The max length of this field is 500')])
    submit = SubmitField("Send")

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
                       