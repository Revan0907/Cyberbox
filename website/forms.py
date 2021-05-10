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

class PaymentForm(FlaskForm):
    address = StringField('Shipping Adress', validators=[DataRequired(), Regexp('^.{1,200}$', message='Shipping Address must be below 200 characters.')])
    cardnum = StringField('Card Number', validators=[DataRequired(), Regexp('^[0-9]{16}$', message='Card number must be 16 digits only')])
    expmonth = StringField('Expiration month', validators=[DataRequired(), Regexp('^(1[0-2]|[1-9]|0[1-9])$', message='Card expiration month must be a number between 1-12')])
    expyear = StringField('Expiration year', validators=[DataRequired(), Regexp('^(202[1-9]|20[3-5][0-9])$', message='Year must be a 4 digit number between 2021-2059')])
    cvv = StringField('CVV', validators=[DataRequired(), Regexp('^[0-9]{3}$', message='CVV must be 3 digit number')])
    submit = SubmitField('Pay')
