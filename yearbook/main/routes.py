from flask import render_template, Blueprint, request, url_for, redirect
from yearbook.main.forms import MessageForm
from yearbook.image_processing.utils import create_images
from os import listdir
from yearbook import insert_messages, view_messages

from PIL import Image

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():

    message = MessageForm()

    if message.validate_on_submit():  # if it is valid, goes here

        # adds to the messages global variable
        insert_messages(message.message.data, message.message.name)

    all_messages = view_messages()

    images = create_images(all_messages)

    return render_template('main.html', title='Yearbook', images=images, messageForm=message,
                           messages=all_messages, messages_length=len(all_messages), images_length=len(images))
