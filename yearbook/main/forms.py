from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, Length

class MessageForm(FlaskForm):
    name = StringField('Name')
    message = TextAreaField('Message')

    submitMessage = SubmitField('Add Message')

    def validate_name(self, name):
        if not name.data:
            raise ValidationError("Cannot leave blank!")


    def validate_message(self, message):
        if not message.data:
            raise ValidationError("Cannot leave blank!")

# class GenerateImageForm(FlaskForm):

#     submitImageGeneration = SubmitField("Generate Images!")