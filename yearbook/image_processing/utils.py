import random

# this file will create the necessary images, and then return that image based on a list of texts
# has all the helper methods 

# texts is a list that contains both messages and authors
def create_images(texts = []): 

    images = []

    size = (1048,1048)

    from PIL import Image, ImageDraw, ImageFont

    for msg, author in texts:

        txt = Image.new('RGBA', size, (255,255,255,255))

        fnt = ImageFont.truetype('yearbook/fonts/Cherolina.ttf', 40)

        d = ImageDraw.Draw(txt)
        # d.text((0, 10), msg, font=fnt, fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))
        d.multiline_text((0, 10), msg, font=fnt, fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))
        txt.save(f'yearbook/modified/wrote_message{author}.png')

        print(d.multiline_textsize(msg, font=fnt))

    return images
