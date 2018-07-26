# -*- coding: utf-8 -*-
"""
Created on Wed May 24 21:38:32 2017

@author: Daniel
"""


def hor_dist(u1, u2):
    # if u2 left of u1, then dist is negative
    l1 = max([v.y  for v in u1[1]])
    r2 = min([v.y for v in u2[1]])
    d1 = l1 - r2
    # if u2 right of u1, then dist is positive
    r1 = min([v.y for v in u1[1]])
    l2 = max([v.y for v in u2[1]])
    d2 = r1 - l2
    # return +/-0.5 if intersecting
    if abs(d1) < abs(d2):
        return min(d1, -0.5)
    else:
        return max(d2, 0.5)
    
def vert_dist(u1, u2):
    # if u2 under u1, then dist is negative
    l1 = max([v.x  for v in u1[1]])
    r2 = min([v.x for v in u2[1]])
    d1 = l1 - r2
    # if u2 right of u1, then dist is positive
    r1 = min([v.x for v in u1[1]])
    l2 = max([v.x for v in u2[1]])
    d2 = r1 - l2
    # return +/-0.5 if intersecting
    if abs(d1) < abs(d2):
        return min(d1, -0.5)
    else:
        return max(d2, 0.5)  
    
    
    
    
    
    
    