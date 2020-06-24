from flask import render_template, Blueprint, request, url_for, redirect
from yearbook.main.forms import MessageForm, GenerateImageForm
from yearbook.image_processing.utils import create_images
from os import listdir

from PIL import Image

main = Blueprint('main', __name__)

messages = []
images = []


@main.route('/', methods=['GET', 'POST'])
def index():

    message = MessageForm()

    generate_image = GenerateImageForm()

    if message.validate_on_submit():  # if it is valid, goes here

        # adds to the messages global variable
        messages.append((message.message.data, message.name.data))

    messages_length = len(images)

    return render_template('main.html', title='Yearbook', images=images, messageForm=message,
                           generate_image=generate_image, messages=messages, messages_length=messages_length)


# just want to let the users post to this route, to generate the image
@main.route('/generate_image', methods=['POST'])
def generate_image_route():

    if request.method == 'POST':

        # then we want to create the images -> and add in the new images
        # by editing the images globally
        images.extend(create_images(messages))

        # we want to clear the messages after we create the new ones
        messages.clear()

    # then we want to redirect to the main index
    return redirect(url_for('main.index'))
