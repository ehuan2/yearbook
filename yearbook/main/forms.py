from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, Length

class MessageForm(FlaskForm):
    name = StringField('Name')
    message = TextAreaField('Message')

    submitMessage = SubmitField('Add Message')
    generateImage = SubmitField('Generate Images')