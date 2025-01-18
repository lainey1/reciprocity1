from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User


def user_exists(form, field):
    # Checking if user exists
    email_or_username = field.data
    # user = User.query.filter(User.email == email).first()
    user = User.query.filter(
        (User.email == email_or_username) | (User.username == email_or_username)
    ).first()

    if not user:
        raise ValidationError('Email or username provided not found.')


def password_matches(form, field):
    # Checking if password matches
    password = field.data
    email_or_username = form.data['email_or_username']
    user = User.query.filter(
        (User.email == email_or_username) | (User.username == email_or_username)
    ).first()
    if not user:
        raise ValidationError('No such user exists.')
    if not user.check_password(password):
        raise ValidationError('Password was incorrect.')


class LoginForm(FlaskForm):
    email_or_username = StringField('email or username', validators=[DataRequired(), user_exists])
    password = StringField('password', validators=[DataRequired(), password_matches])
