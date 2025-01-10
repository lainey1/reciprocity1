from flask_wtf import FlaskForm
from wtforms import SubmitField

class DeleteUserForm(FlaskForm):
    delete = SubmitField('Delete Profile')
    cancel = SubmitField('Cancel')
