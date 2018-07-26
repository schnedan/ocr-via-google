# -*- coding: utf-8 -*-
"""
Created on Thu May 25 12:12:38 2017

@author: Daniel
"""

from distance import hor_dist, vert_dist
import string

def find_start_char(k, chars):
    # put keyword into nice shape
    keyword = list()
    m = [c for c in chars if c[0] == k[0][0] and contained(c, k)]
    m.sort(key=lambda x: box_center(x[1])[1], reverse=True)
    m = [c for c in m if on_same_spot(c, m[0])]
    c = choose_best_char(m)
    while c and contained(c, k):
        keyword.append(c)
        c = find_next_char(c, chars)
    c = find_next_char(keyword[-1], chars)
    while c and c[0] in string.punctuation:
        c = find_next_char(c, chars)
    if c:
        return c
    c = next_line([keyword, list()], chars)
    


def find_next_char(char, chars, direction='right', bound=False):
    """ returns a single char or False if found none
    If bound is given, then one will not search further
    than this bound. Still to work out!
    """
    if direction in ['right', 'left']:
        sign = 1 if direction == 'right' else -1
        pre_sel = [(c, sign*hor_dist(char, c)) for c in chars if sign*hor_dist(char, c) > 0 and on_same_line(char, c)]
    if direction in ['down', 'up']:
        sign = 1 if direction == 'up' else -1
        bh = box_width(char[1])
        pre_sel = [(c, sign*vert_dist(char, c)) for c in chars if (sign*vert_dist(char, c) >= 1 
                    and abs(hor_dist(char, c)) <= 2*bh) and not on_same_line(char, c)]
    pre_sel.sort(key=lambda x: x[1])
    while len(pre_sel) > 0 and (on_same_spot(char, pre_sel[0][0]) 
            or contained(pre_sel[0][0], char)):
        del pre_sel[0]
    if len(pre_sel) == 0:
        return False
    candidates = list()
    candidates.append(pre_sel[0][0])
    del pre_sel[0]
    while len(pre_sel) > 0 and on_same_spot(candidates[0], pre_sel[0][0]):
        candidates.append(pre_sel[0][0])
        del pre_sel[0]
    return choose_best_char(candidates)

def next_line(a, chars, direction='down'):
    m = [find_next_char(c, chars, direction=direction) for c in a[0] if c is not False]
    m = [c for c in m if c is not False]
    if len(m) == 0:
        return False
    sign = 1 if direction == 'up' else -1
    m.sort(key=lambda x: min([sign*vert_dist(c, x) for c in a[0] if sign*vert_dist(c, x) >= 1]))
    ll = list()
    c = m[0]
    while c:
        ll.append(c)
        c = find_next_char(c, chars, direction = 'left')
        if c is not False and abs(hor_dist(c, ll[-1])) >= 2*sum([box_width(ch[1]) for ch in ll])/len(ll):
            c = False
    return ll[-1]
    
    

def choose_best_char(candidates):
    """ returns a single char
    To work out. This function gives for example ä priority over a, 
    é priority over e, etc.
    """
    cc = [c[0].lower() for c in candidates]
    cc = list(set(cc))
    if len(cc) == 1:
        return candidates[0]
    # ü has priority, e.g. over u and i; etc
    for uml in ['ü', 'ä', 'ö', 'é', 'è', 'à', 'ô', 'ç']:
        if uml in cc:
            candidates = [c for c in candidates if c[0].lower() == uml]
            break
    if len(candidates) > 1 and 'a' in cc and 'h' in cc:
        candidates = [c for c in candidates if c[0].lower() == 'h']
    if len(candidates) > 1 and '-' in cc and '.' in cc:
        candidates = [c for c in candidates if c[0].lower() == '-']
    return candidates[0]
    
def on_same_spot(char1, char2):
    """ returns True/False
    This is a primitive approach:
    In order to return True, each center
    has to lie inside the bounding rectangle
    of the other box.
    Still to check how it works in the different contexts!
    """
    c1 = box_center(char1[1])
    c2 = box_center(char2[1])
    if (c2[0] <= min([v.x for v in char1[1]]) 
        or c2[0] >= max([v.x for v in char1[1]])):
            return False
    if (c2[1] <= min([v.y for v in char1[1]])  
        or c2[1] >= max([v.y for v in char1[1]])):
            return False
    if (c1[0] <= min([v.x for v in char2[1]]) 
       or  c1[0] >= max([v.x for v in char2[1]])):
            return False
    if (c1[1] <= min([v.y for v in char2[1]]) 
        or c1[1] >= max([v.y for v in char2[1]])):
            return False
    return True

def on_same_line(c1, c2):
    """
    At least one character should have the following property:
    At least 1/3 of its vertical length is shadowed by the 
    other character. This might exclude cases like g'. 
    To treat!
    """
    common_height = (min(max([v.x for v in c1[1]]), max([v.x for v in c2[1]])) 
        - max(min([v.x for v in c1[1]]), min([v.x for v in c2[1]])))
    if common_height >= min(box_height(c1[1]), box_height(c2[1])) / 3:
        return True
    return False

def contained(char, word):
    """ returns True/False
    In order to return True, the center of char
    has to lie inside the bounding rectangle of word.
    """
    c1 = box_center(char[1])
    if (c1[0] <= min([v.x for v in word[1]]) 
       or  c1[0] >= max([v.x for v in word[1]])):
            return False
    if (c1[1] <= min([v.y for v in word[1]]) 
        or c1[1] >= max([v.y for v in word[1]])):
            return False
    return True


def box_center(b):
    c1 = mid_coord(b[0], b[2])
    c2 = mid_coord(b[1], b[3])
    return mid_coord(c1, c2)
    
def mid_coord(t1, t2):
    if isinstance(t1, tuple):
        x1, y1, x2, y2 = (t1[0], t1[1], t2[0], t2[1])
    else:
        x1, y1, x2, y2 = (t1.x, t1.y, t2.x, t2.y)
    return (round((x1+x2) / 2), round((y1+y2) / 2))


def box_width(b):
    ll = [v.y for v in b]
    ll.sort()# attention: order of vertices might be mixed up
    return round((ll[3] + ll[2] - ll[1] - ll[0]) / 2)

def box_height(b):
    ll = [v.x for v in b]
    ll.sort()# attention: order of vertices might be mixed up
    return round((ll[3] + ll[2] - ll[1] - ll[0]) / 2)


