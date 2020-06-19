from flask import render_template, Blueprint, request, url_for, redirect
from yearbook.main.forms import MessageForm, GenerateImageForm
from yearbook.image_processing.utils import create_images
from os import listdir

from PIL import Image

main = Blueprint('main', __name__)

messages = []


@main.route('/', methods=['GET', 'POST'])
def index():

    message = MessageForm()

    generate_image = GenerateImageForm()

    if message.validate_on_submit():  # if it is valid, goes here

        # adds to the messages global variable
        messages.append((message.message.data, message.name.data))

    images = [f for f in listdir("./yearbook/static/modified")]

    return render_template('main.html', title='Yearbook', images=images, messageForm=message, generate_image=generate_image, messages=messages)


@main.route('/generate_image', methods=['GET', 'POST'])
def generate_image_route():

    message = MessageForm()

    generate_image = GenerateImageForm()

    if generate_image.validate_on_submit():
        create_images(messages)
        messages.clear()

    images = [f for f in listdir("./yearbook/static/modified")]

    return redirect(url_for('main.index'))
