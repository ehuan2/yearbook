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

    if message.validate_on_submit():

        if message.submitMessage.data:
            messages.append((message.message.data, message.name.data))
        
        if message.generateImage.data:
            create_images(messages)


    images = [f for f in listdir("./yearbook/static/modified")]

    return render_template('main.html', title='Yearbook', images=images,
                           messageForm=message, messages=messages)