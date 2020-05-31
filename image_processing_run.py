from yearbook.image_processing.utils import create_images
import time

if __name__ == '__main__':

    start = time.perf_counter()
    
    messages = [('hello test test stestse tseo stetsetset\nFrom,\nEric', 'eric'), 
    ('fdsafdsafsadfsdfsdfsdsdfsd nope test1 test2', 'me'), ('more examples from me :) are coming now', 'hello'), 
    ('why not? Because I said so lol', 'here'), ('okay okay okay hehehe hehehe', 'now'), 
    ('test test test, test, test, test', 'yes')]
    

    create_images(texts = messages)

    finish = time.perf_counter()

    print(f'Algorithm took: {finish - start} second(s)\n')
