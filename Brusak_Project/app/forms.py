from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp

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