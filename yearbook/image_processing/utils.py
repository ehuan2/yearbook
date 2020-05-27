from PIL import Image, ImageDraw, ImageFont
import random

# this file will create the necessary images, and then return that image based on a list of texts
# has all the helper methods 

# texts is a list that contains both messages and authors
def create_images(texts = []): 

    images = []

    size = (1048,1048)

    for msg, author in texts:

        txt = Image.new('RGBA', size, (255,255,255,255))

        fnt = ImageFont.truetype('yearbook/fonts/Cherolina.ttf', 40)

        d = ImageDraw.Draw(txt)
        # d.text((0, 10), msg, font=fnt, fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))
        # d.multiline_text((0, 10), msg, font=fnt, fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))
        # txt.save(f'yearbook/modified/wrote_message{author}.png')
        
        string = find_best_string(message = msg.split(' '), font = fnt, d = d)

        print(string)
        print(d.multiline_textsize(string, font=fnt))
        print()


    return images


# Steps for DP:
# 1. Define Subproblem, just a suffix [i:]
# 2. Guess, where to place a space
# 3. Relate Subproblems, min(area of one, vs area of another)
# 4. Memoize or Tabulate
# 5. Return Orig. Problem

# creating a method that returns the area
def find_area(area : tuple) -> int:
    return area[0] * area[1]

counter = 0

# we need a method that returns the best dimensions for the text, we need to determine when to add in a new line
# will need to take use of a dictionary and memoization
def find_best_string(message = [], pos = 0, font = None, d = None, size_restrictions = 311, memoize = {}):

    # print(message)
    # print()
    global counter 
    counter += 1
    # print(counter)

    if pos == len(message):

        entire_string = ''''''

        for msg in message:
            entire_string += msg if "\n" in msg else msg + " "

        return entire_string

    answers = [find_best_string(message=message[0:pos] + [f'''{message[pos]}\n'''] + message[pos+1:len(message)], pos = pos+1, font = font, d = d, memoize=memoize),
    find_best_string(message=message[0:pos] + [f'''{message[pos]}'''] + message[pos+1:len(message)], pos = pos+1, font = font, d = d, memoize=memoize)]

    if answers[0] == 'Could not resize it!' and answers[1] == 'Could not resize it!':
        print("Really couldn't resize it!")
        exit()

    elif answers[0] == 'Could not resize it!':
        return answers[1]

    elif answers[1] == 'Could not resize it!':
        return answers[0]

    area0 = d.multiline_textsize(answers[0], font = font)
    area1 = d.multiline_textsize(answers[1], font = font)

    if area0[0] > size_restrictions and area1[0] > size_restrictions:
        return "Could not resize it!"

    elif area0[0] > size_restrictions:
        memoize[pos] = answers[1]
        return answers[1]
    elif area1[0] > size_restrictions:
        memoize[pos] = answers[0]
        return answers[0]


    if find_area(area0) >= find_area(area1):        
        memoize[pos] = answers[1]
        return answers[1]
    else:
        memoize[pos] = answers[0]
        return answers[0]