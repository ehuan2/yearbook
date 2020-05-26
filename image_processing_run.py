from yearbook.image_processing.utils import create_images

if __name__ == '__main__':
    messages = [['''hello test test stestsetestsetse tsetsetsethellohello 
    stetsetset testsetse tsetsetsetsets \nsetsetsetsetsetset''', 'from eric'],['nope', 'from me']]
    create_images(texts = messages)