#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 20:29:19 2017

@author: Daniel
"""

import glob
from getVision import vision_call, digest_vision
from char import find_start_char, find_next_char, on_same_line, box_width, box_height, next_line, contained
from distance import hor_dist, vert_dist
#from sklearn.neighbors import NearestNeighbors
from statistics import mean
import re


train_files = glob.glob('./*.jpg')
path = train_files[-2]

rotation_right = False
while not rotation_right:
    # do several calls to google vision
    # increases changes of finding spezial characters
    visions = list()
    visions.append(vision_call(path))
    visions.append(vision_call(path, language_hints=['de']))
    visions.append(vision_call(path, language_hints=['fr']))
    
    # digest visions
    words = list()
    chars = list()
    for vi in visions:
        words = words + digest_vision(vi, level='words')
        chars = chars + digest_vision(vi, level='chars')
        
    # check if rotation is right

def get_ingredients(words, chars, language='de'):
    keyword = 'zutaten'# to define for other languages
    k = [w for w in words if keyword in w[0].lower()]
    if len(k) == 0:# case still to treat with different occurances of keyword
        return False
    if len(k) > 1:
        kk = [w for w in k if find_next_char(w, chars) and find_next_char(w, chars)[0] == ':']
    if len(kk):
        k = kk[0]
    else:
        k = k[0]
    c = find_start_char(k, chars)
    if c is False:
        return False
    ii = list()
    ing_list = list()
    ing_list.append(['', [''], ''])
    sep = list()
    sep.append([0, 'new_line'])
    ingredient_starting = True
    ingredient_ending = False
    line_starting = False
    right_bound = False
    parents = {i for i, w in enumerate(words) if contained(c, w)}
    while c:
        ii.append(c)
        # check for start of ingredient
        if c[0] in ['(', '[']:
            if not ingredient_starting:
                ing_list.append(['', [''], ''])
                ingredient_starting = True
            ing_list[-1][0] += c[0]
        elif ingredient_starting:
            ingredient_starting = False
        # check for end of ingredient
        if c[0] in [',', ':', ';', '.', ')', ']']:
            if len([w for w in words if contained(c, w) and len(w[0]) > 1]) == 0:
                ingredient_ending = True
                ing_list[-1][2] += c[0]
        elif ingredient_ending:
            # stopping rule: last line too short
            if line_starting and len(ii) != sep[-1][0] + 1:
                if (min([v.y for v in ii[sep[-1][0] - 1][1]]) - right_bound 
                        > (max([v.y for v in ii[sep[-1][0]][1]]) - min([v.y for v in ii[-1][1]]))):
                    del ing_list[-1]# to correct! if last line does not end with . or ,
                    ii = ii[:(sep[-1][0] - 1)]
                    print('last line too short.')
                    break
                else:
                    line_starting = False
    
            ingredient_ending = False
            # add comma if forgotten. To take away afterwards if last ingredient.
            if ii[-1][0] in [')', ']']:
                ing_list[-1][2] += ','
            ingredient_starting = True
            parents = {i for i, w in enumerate(words) if contained(c, w)}
            ing_list.append(['', [''], ''])
            ing_list[-1][1][0] += c[0]
        # otherwise add character to ingredient
        if not ingredient_starting and not ingredient_ending:
            # check if one should add whitespace
            parents_next = {i for i, w in enumerate(words) if contained(c, w)}
            if len(parents.intersection(parents_next)) == 0:
                parents = parents_next
                if len(ing_list[-1][1][0]) and c[0] not in ['%', '-', '/'] and ii[-2][0] != '/':
                    ing_list[-1][1][0] += ' '
                    # stopping rule: last line too short
                    if line_starting and len(ii) != sep[-1][0] + 1:
                        if (min([v.y for v in ii[sep[-1][0] - 1][1]]) - right_bound 
                                > (max([v.y for v in ii[sep[-1][0]][1]]) - min([v.y for v in ii[-1][1]]))):
                            del ing_list[-1]# to correct! if last line does not end with . or ,
                            ii = ii[:(sep[-1][0] - 1)]
                            print('last line too short.')
                            break
                        else:
                            line_starting = False
            ing_list[-1][1][0] += c[0]
        
        # stopping rule: french "ingredient"
        if re.search('ingr[ée]d[il]ent', to_string(ii).lower()):# 'ingrédient' in to_string(ii).lower() or 'ingredient' in to_string(ii).lower():
            del ii[-10:]
            del ing_list[-1]
            print('ingrédient encountered')
            break
        c1 = find_next_char(c, chars)
        # check for new line
        if c1 is not False and c1[0] == '%' and c[0] == c1[0]:
            c = find_next_char(c1, chars)
        else:
            c = c1
        if c is not False and (abs(hor_dist(ii[-1], c)) >= 2*sum([box_width(ch[1]) for ch in ii])/len(ii) 
                or box_height(c[1]) >= 1.5 * mean([box_height(d[1]) for d in ii])):
            c = False
            print('end of line')
            #break
        if c is False:
            print('going to next line ' + str(len(ii)) + '  ')
            if len(sep) == 1 and on_same_line(k, ii[0]):
                c = next_line([[k], sep], chars)
            else:
                c = next_line([ii[sep[-1][0]:min(sep[-1][0] + 5, len(ii))], sep], chars)
            #break
            if c is not False:
                sep.append([len(ii), 'new_line'])
                line_starting = True
                if right_bound:
                    right_bound = min(right_bound, min([v.y for v in ii[-1][1]]))
                else:
                    right_bound = min([v.y for v in ii[-1][1]])
    return ing_list

    if False:
        # finding white spaces
        count = 0
        while count <= len(ii) - 2:
            m = {i for i, w in enumerate(words) if contained(ii[count], w)}
            m2 = m
            while count <= len(ii) - 2 and (len(m.intersection(m2)) 
                    or ii[count][0] in [',', ')', ']', ':', ';', '.', '-', '\'', '%', '/']):
                count = count + 1
                m2 = {i for i, w in enumerate(words) if contained(ii[count], w)}
            if count == len(ii) - 1:
                break
            if ii[count - 1][0] not in ['(', '/']:
                sep.append([count-1, 'white_space'])
        if False:
            for i in range(1, len(ii) - 1):
                if hor_dist(ii[i], ii[i+1]) >= 2 * mean([box_width(c[1]) for c in ii[max(0, i-3):i]]) / 3:
                    sep.append([i, 'white_space'])
        # cut off stuff
        # white space at end of line is longer than first word on new line
        sepp = [sp for sp in sep if sp[0] != 0 and sp[1] == 'new_line']
        if len(sepp) > 1:
            right_bound = min([v.y for v in ii[sepp[0][0] - 1][1]])
            for i in range(1, len(sepp)):
                wsp = [sp for sp in sep if sp[0] >= sepp[i][0] and sp[1] == 'white_space']
                if len(wsp) == 0:
                    break
                if (min([v.y for v in ii[sepp[i][0] - 1][1]]) - right_bound 
                        > (max([v.y for v in ii[sepp[i][0]][1]]) - min([v.y for v in ii[wsp[0][0]][1]]))):
                    del ii[sepp[i][0]:len(ii)]
                    break
                else:
                    right_bound = min(right_bound, min([v.y for v in ii[sepp[i][0] - 1][1]]))
        

    
def to_string(ii):
    ss = [c[0] for c in ii]
    s = ''
    #wsp =[sp[0] for sp in sep if sp[1] == 'white_space']
    for i,t in enumerate(ss):
        s += t
        #if i in wsp:
        #    s += ' '
    return s


ss = [c[0] for c in ii]
s = ''
wsp =[sp[0] for sp in sep if sp[1] == 'white_space']
for i,t in enumerate(ss):
    s += t
    if i in wsp:
        s += ' '
s


import io
from PIL import Image, ImageDraw
from google.cloud import vision

vision_client = vision.Client('coop_zutaten')
# Loads the image into memory
with io.open(path, 'rb') as image_file:
    content = image_file.read()
    image = vision_client.image(content=content)

def draw_boxes(image, blocks, color, full=True):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)
    if full:
        for block in blocks:
            draw.polygon([
                block.vertices[0].x, block.vertices[0].y,
                block.vertices[1].x, block.vertices[1].y,
                block.vertices[2].x, block.vertices[2].y,
                block.vertices[3].x, block.vertices[3].y], None, color)
    else:
          for block in blocks:
            draw.polygon(block[1], None, color)

    return image

# Collect specified feature bounds by enumerating all document features
img = Image.open(path)
bounds = []
# for detect_text
bounds = digest_vision(doc)
img = draw_boxes(img, bounds, color = 'yellow', full=False)
# for detect_full_text
for page in visions[1].pages:
    for block in page.blocks:
        for paragraph in block.paragraphs:
            for word in paragraph.words:
                for symbol in word.symbols:
                    bounds.append(symbol.bounding_box)
img = draw_boxes(img, bounds, color = 'yellow')
img.show()
