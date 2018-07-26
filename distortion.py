# -*- coding: utf-8 -*-
"""
Created on Thu May 25 23:48:33 2017

@author: Daniel
"""

from char import box_width, box_height

def is_rotated(word_list):
    """ False or True
    For the moment check only the word Zutaten 
    and only rotation of 90 degree.
    """
    zz = [w[1] for w in word_list if 'zutaten' in w[0].lower()]
    if len(zz):
        box = zz[0]
        if box_width(box) < box_height(box):
            return True
    return False

def round_object(char_list):
    """ False or True
    Study how consecutive characters are
    situated and determine if object 
    is round or not. To work out.
    """
    return False