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
        insert_messages(message.message.data)


    all_messages = view_messages()
    print(all_messages)
    # create_images(all_messages)


    return render_template('main.html', title='Yearbook', images=[], messageForm=message,
                           messages=all_messages, messages_length=0)


# just want to let the users post to this route, to generate the image
# @main.route('/generate_image', methods=['POST'])
# def generate_image_route():

#     if request.method == 'POST':

#         # then we want to create the images -> and add in the new images
#         # by editing the images globally

#         new_images = create_images(messages)

#         for img in new_images:
#             insert_images(img)

#         images.extend(create_images(messages))

#         # we want to clear the messages after we create the new ones
#         messages.clear()

#     # then we want to redirect to the main index
#     return redirect(url_for('main.index'))