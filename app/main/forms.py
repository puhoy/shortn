__author__ = 'meatpuppet'


from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, URL, Length

class SubmitLinkForm(Form):
    """
    form for the link shortening
    """
    link = StringField('', validators=[DataRequired()])  # the placeholder is specified in main_index.html
    submit = SubmitField('s!')