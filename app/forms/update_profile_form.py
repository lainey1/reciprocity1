# /forms/update_profile_form

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Optional, Length

class UpdateProfileForm(FlaskForm):
    first_name = StringField('first name', validators=[InputRequired()])
    location = StringField('city, state', validators=[InputRequired(), Length(max=255)])
    bio = TextAreaField('about me', validators=[InputRequired()])
    profile_image_url = StringField('paste profile picture URL', validators=[Optional()])
