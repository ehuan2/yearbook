from flask import render_template, Blueprint, request, url_for
from yearbook.main.forms import MessageForm
from yearbook.image_processing.utils import create_images
from os import listdir

from PIL import Image

main = Blueprint('main', __name__)

messages = []


@main.route('/', methods=['GET', 'POST'])
def index():

    message = MessageForm()

    validate = ""

    if message.validate_on_submit():  # if it is valid, goes here

        if message.submitMessage.data:  # adds message if it's from the submit message portion

            # checks if the messages are valid
            validate = message.check_validation(
                nme=message.name.data, msg=message.message.data)

            if not validate:
                messages.append((message.message.data, message.name.data))

        if message.generateImage.data:  # generates image if that is the button pressed -> no else in case of post through other sources
            create_images(messages)

    images = [f for f in listdir("./yearbook/static/modified")]

    return render_template('main.html', title='Yearbook', images=images, validate=validate,
                           messageForm=message, messages=messages)
