from flask_login import current_user
from flask_wtf import FlaskForm  
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
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

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("Please enter your name."), Length(min=4, max=14, message ='Length of this field must be between 4 and 14')])
    email = StringField('Email', validators=[DataRequired("Please enter your email."), Email("Please enter correct email")])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField("About me", validators=[Length(max=120, message='Max length is 120')])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError('This username is taken.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('This email is taken.')

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old password')
    new_password = PasswordField('New password',
                             validators=[Length(min=6,
                                                message='Password must be longer then 6')])
    confirm_password = PasswordField('Confirm new password',
                                     validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("Reset password")

    def validate_old_password(self, old_password):
        if not current_user.verify_password(old_password.data):
            raise ValidationError('Wrong password. Try again!')