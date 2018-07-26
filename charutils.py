# -*- coding: utf-8 -*-
"""
Created on Tue May 23 13:42:33 2017

@author: Daniel
"""

from statistics import median
from rect_union import createUnionFilledRect

def get_char_height(word_list):
    one_line_str = [w for w in word_list if '\n' not in w[0]]
    hight_list = [w[1][3] for w in one_line_str]
    return(int(median(hight_list)))
    
def get_zutaten_coord(word_list):
    one_line_str = [w for w in word_list if '\n' not in w[0]]
    zu_str = [w for w in one_line_str if 'zutaten' in w[0].lower()]
    if len(zu_str) == 1:
        x, y, w, h = zu_str[0][1]
        return((x, y))
    else:
        return(False)
    
def eliminateNoneText(word_list, gray):
    one_line_rects = [w[1] for w in word_list if '\n' not in w[0]]
    ru = createUnionFilledRect(one_line_rects, gray.shape, enlarge = get_char_height(word_list))
    gray[ru == 0] = 255
    return(gray)

def eliminateNoneTextRects(word_list, gray, rects):
    one_line_rects = [w[1] for w in word_list if '\n' not in w[0]]
    ru = createUnionFilledRect(one_line_rects, gray.shape, enlarge = get_char_height(word_list))
    rects = [rect for rect in rects if (ru[rect[1]:(rect[1] + rect[3]), rect[0]:(rect[0] + rect[2])] == 255).any()]
    return(rects)
 
def enlargeRects(rects, char_height, gray_shape):
    out = list()
    delta = round(char_height / 5)
    for rect in rects:
        x1 = max(0, rect[0] - delta)
        x2 = min(gray_shape[1], rect[0] + rect[2] + delta)
        y1 = max(0, rect[1] - delta)
        y2 = min(gray_shape[0], rect[1] + rect[3] + delta)
        out.append((x1, y1, x2 - x1, y2 - y1))
    return(out)


