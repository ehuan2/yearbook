from PIL import Image, ImageDraw, ImageFont
import concurrent.futures
import random

# this file will create the necessary images, and then return that image based on a list of texts
# has all the helper methods

# texts is a list that contains both messages and authors
def create_images(texts=[]):

    if len(texts) < 10: # if the data is small enough, does it synchronously
        
        for text in texts:
            process_images(text)
    
    else: # does it asynchronously if the data pool is bigger
        
        # parallel processing version, better when handling larger quantities of data
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(process_images, texts)


# do processing of images here now, here is the method to call:
def process_images(messages=[]):

    size = (1024, 1024) # default size 

    msg, author = messages # gets the message and author here

    txt = Image.new('RGBA', size, (255, 255, 255, 255))
    fnt = ImageFont.truetype('yearbook/fonts/Orange_Juice.ttf', 40)

    d = ImageDraw.Draw(txt)

    # gets the message
    message = find_best_string(message=msg.split(' '), pos = 0, font=fnt, d=d, size_x = size[0]/4, size_y = size[1]/4, memo = {})

    if message == 'Could not resize it!':
        return None

    d.multiline_text((0, 10), message, font=fnt, fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255),255))

    txt.save(f'yearbook/modified/wrote_message{author}.png')


# Steps for DP:
# 1. Define Subproblem, just a suffix [i:]
# 2. Guess, where to place a space
# 3. Relate Subproblems, min(area of one, vs area of another)
# 4. Memoize or Tabulate
# 5. Return Orig. Problem
def find_best_string(message=[], pos=0, font=None, d=None, size_x=300, size_y = 300, memo = {}):

     # if it is already memoized, it goes here
    if memo.get(pos):
        return memo.get(pos)

    # it's -1 and not len(message) because we don't care if the last one has a new line, 1/2 the time
    if pos == len(message) - 1:
        memo[pos] = message[pos]
        return message[pos]

    # creates both possibilities
    answers = [f'''{message[pos]}\n''' + find_best_string(message=message, 
    pos=pos+1, font=font, d=d, memo = memo),
            f'''{message[pos]} ''' + find_best_string(message=message, 
    pos=pos+1, font=font, d=d, memo = memo)]

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