# /forms/update_profile_form

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Optional, Length

class UpdateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    location = StringField('City, State', validators=[InputRequired(), Length(max=255)])
    bio = TextAreaField('About Me', validators=[InputRequired()])
    profile_image_url = StringField('Profile Picture', validators=[Optional()])
