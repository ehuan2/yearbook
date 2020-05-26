import random

# this file will create the necessary images, and then return that image based on a list of texts
# has all the helper methods 

# texts is a list that contains both messages and authors
def create_images(texts = []): 

    images = []

    size = (480,480)

    from PIL import Image, ImageDraw, ImageFont

    for msg, author in texts:

        txt = Image.new('RGBA', size, (255,255,255,255))

        fnt = ImageFont.truetype('fonts/Orange_Juice.ttf', 40)

        d = ImageDraw.Draw(txt)
        d.text((240, 10), msg, font=fnt, fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))
        txt.save(f'modified/wrote_message{author}.png')

    return images
