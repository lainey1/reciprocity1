from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from app.models import User


def user_exists(form, field):
    # Checking if user exists
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        raise ValidationError('Email address is already in use.')


def username_exists(form, field):
    # Checking if username is already in use
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError('Username is already in use.')



class SignUpForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), user_exists, Email()])
    username = StringField(
        'username', validators=[DataRequired(), username_exists])
    first_name = StringField('first name', validators=[DataRequired(), Length(max = 70)])
    password = StringField('password', validators=[DataRequired(),Length(min = 6)])
