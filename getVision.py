# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:37:07 2017

@author: Daniel
"""
import io

# Imports the Google Cloud client library
from google.cloud import vision

def vision_call(path, full=True, language_hints=None):
    # Instantiates a client
    # Don't know if necessary (in terminal): set GCLOUD_PROJECT=coop_zutaten
    vision_client = vision.Client('coop_zutaten')
    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(content=content)
    
    if full == False:
        return image.detect_text()
    else:
        return image.detect_full_text(language_hints=language_hints)
    
def digest_vision(vision, level='words'):
    """ return list of words/characters with their bounding boxes
    Attention: In the tutorial of vision vertices in a box should alway start 
    on the upper left corner and then continue clockwise. But 
    it seems like that while this is the case for words, it is 
    not the case for symbols (characters) where the vertices tend to 
    start on the upper right corner!
    """
    if (type(vision) == type(list())):
        if False:
            chars = list()
            for char_count, char in enumerate(vision):
                chars.append(list())
                chars[char_count].append(char.description)
                chars[char_count].append(char.bounds.vertices)
            return chars
        if False:
            word_list = list()
            for text in vision:
                vertices = ([(bound.x_coordinate, bound.y_coordinate)
                            for bound in text.bounds.vertices])
                rect = (vertices[0][0], vertices[0][1], vertices[1][0] - vertices[0][0], vertices[2][1] - vertices[0][1])
                word_list.append([text.description, rect])
            return word_list
        if True:
            word_list = list()
            for text in vision:
                vertices = ([(bound.x_coordinate, bound.y_coordinate)
                            for bound in text.bounds.vertices])
                poly = [vertices[0][0], vertices[0][1], vertices[1][0], vertices[1][1], vertices[2][0], vertices[2][1], vertices[3][0], vertices[3][1]]
                word_list.append([text.description, poly])
            return word_list
    elif level == 'words':
        words = list()
        word_count = 0
        for page in vision.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        ww = get_word_text(word)
                        words.append(list())
                        words[word_count].append(ww)
                        words[word_count].append(word.bounding_box.vertices)
                        word_count += 1
        return words
    elif level == 'chars':
        chars = list()
        char_count = 0
        for page in vision.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            chars.append(list())
                            chars[char_count].append(symbol.text)
                            chars[char_count].append(symbol.bounding_box.vertices)
                            char_count += 1
        return chars
    else:
        return False

def get_word_text(word):
    word_text = ''
    for s, symbol in enumerate(word.symbols):
        word_text = word_text + symbol.text
    return word_text


def zoomed_vision(path, chars):
    box = bounding_box(chars)
    
def bounding_box(path, ii):
    img = Image.open(path)
    left = max([max([v.y for v in c[1]]) for c in ii])
    right = min([min([v.y for v in c[1]]) for c in ii])
    up = min([min([v.x for v in c[1]]) for c in ii])
    down = max([max([v.x for v in c[1]]) for c in ii])
    box = (up, right, down, left)
    img_crop = img.crop(box)
    img_crop.save('img_crop.jpg')
    cropped_vision = vision_call('img_crop.jpg')


