from PIL import Image, ImageDraw, ImageFont
import concurrent.futures
import random
import os
import time

# this file will create the necessary images, and then return that image based on a list of texts
# has all the helper methods

# creating all fonts
all_fonts = [f'./yearbook/fonts/{f}' for f in os.listdir('./yearbook/fonts/')]

# texts is a list that contains both messages and authors
def create_images(texts=[], size=(1044, 1044)):

    # now that we know we can resize stuff, we want to resize it so that we can fit 4 on one page
    txt = Image.new('RGBA', size, (255, 255, 255, 255))
    fnt = ImageFont.truetype('yearbook/fonts/Orange_Juice.ttf', 40)
    d = ImageDraw.Draw(txt)

    # we need a method to just grab all the processed texts
    messages = []
    for text in texts:
        messages.append(process_images((text, txt, fnt, d, size)))

    messages = list(filter(lambda msg: msg, messages))

    # if messages exist, do img processing on them
    if messages:

        for j in range(int(len(messages)/4)+1):

            current_time = time.time()  # get the current time

            # counts the number of actual messages
            count = 0

            # separate the messages into groups of four
            msgs = []

            # loops through, getting all the messages
            for k in range(4):
                if len(messages) > k + j * 4:
                    msgs.append(messages[k+j*4][0])
                    count += 1
                else:
                    msgs.append("")

            # generates the sizes of all the texts
            sizes_of_texts = [d.multiline_textsize(msgs[i], font=fnt)[
                1] for i in range(4)]


            # creating the right sizes now
            new_size = (1044,
                        max(sizes_of_texts[0] + sizes_of_texts[2],
                            sizes_of_texts[1] + sizes_of_texts[3]) + 60)

            # creates new images with new sizes
            txt = Image.new('RGBA', new_size, (255, 255, 255, 255))
            d = ImageDraw.Draw(txt)

            for i in range(count):  # loops through all the

                fnt = ImageFont.truetype(all_fonts[random.randint(0, len(all_fonts)-1)], 40)

                # sets the right positioning
                pos_x = 10 if (i % 2) == 0 else new_size[0]/2
                pos_y = 10 if int(
                    (i % 4) / 2) == 0 else new_size[1] - sizes_of_texts[i % 2 + 1] - 10


                # better generation of colours, so that they aren't too light - their sum has to be < 500
                red = random.randint(0, 255)
                green = random.randint(0, 500 - red)
                blue = random.randint(0, 500 - red - green)

                # writes in the correct text
                d.multiline_text((pos_x, pos_y), msgs[i], font=fnt, fill=(
                    red, green, blue, 255))

            # now saves the text into the pictures based on the current time
            txt.save(
                f'yearbook/static/modified/message_{current_time}.png')


# do processing of images here now, here is the method to call:

def process_images(messages=()):

    whole_msg, txt, fnt, d, size = messages  # gets the message and author here
    msg, author = whole_msg

    # gets the message
    message = find_best_string(message=msg.split(' '), pos=0, font=fnt, d=d, size_x=(
        size[0]-20)/2, size_y=(size[1]-20)/2, memo={})

    if message == 'Could not resize it!':
        return None

    return (message, author)

# Steps for DP:
# 1. Define Subproblem, just a suffix [i:]
# 2. Guess, where to place a space
# 3. Relate Subproblems, min(area of one, vs area of another)
# 4. Memoize or Tabulate
# 5. Return Orig. Problem


def find_best_string(message=[], pos=0, font=None, d=None, size_x=300, size_y=300, memo={}):

    # if it is already memoized, it goes here
    if memo.get(pos):
        return memo.get(pos)

    # it's -1 and not len(message) because we don't care if the last one has a new line, 1/2 the time
    if pos == len(message) - 1:
        memo[pos] = message[pos]
        return message[pos]

    # creates both possibilities
    answers = [f'''{message[pos]}\n''' + find_best_string(message=message,
                                                          pos=pos+1, font=font, d=d, memo=memo),
               f'''{message[pos]} ''' + find_best_string(message=message,
                                                         pos=pos+1, font=font, d=d, memo=memo)]

    # if it is not resizeable for one of them, returns the other one right away
    if answers[0] == 'Could not resize it!':
        memo[pos] = answers[1]
        return answers[1]

    elif answers[1] == 'Could not resize it!':
        memo[pos] = answers[0]
        return answers[0]

    # finds the area of them, to check if it can resize
    area0 = d.multiline_textsize(answers[0], font=font)
    area1 = d.multiline_textsize(answers[1], font=font)

    # shows that it can't be resized here, if one can't, then just returns the other
    if (area0[0] > size_x and area1[0] > size_x) or (area0[1] > size_y and area1[1] > size_y):
        memo[pos] = 'Could not resize it!'
        return 'Could not resize it!'
    elif area0[0] > size_x or area0[1] > size_y:
        memo[pos] = answers[1]
        return answers[1]
    elif area1[0] > size_x or area1[1] > size_y:
        memo[pos] = answers[0]
        return answers[0]

    # the optimal choice is always the one with the least number of lines
    memo[pos] = answers[1]
    return answers[1]
