from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, Email,EqualTo,ValidationError,Regexp, InputRequired
from website.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp('^.{3,15}$', message='Username must be 3 to 15 characters long')])
    firstname = StringField('First name', validators=[DataRequired(), Regexp('^[a-zA-Z]+$', message='First name must only be english letters')])
    lastname = StringField('Last name', validators=[DataRequired(), Regexp('^[a-zA-Z]+$', message='Last name must only be english letters')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{6,8}$', message='Password must be between 6 to 8 characters')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exsists. Please choose a different one')

    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already in use. Please use a different one')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

