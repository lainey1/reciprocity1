from flask_wtf import FlaskForm
from wtforms import SubmitField

class DeleteUserForm(FlaskForm):
    delete = SubmitField('delete profile]')
    cancel = SubmitField('cancel request')
