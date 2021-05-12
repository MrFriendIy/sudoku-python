# -*- coding: utf-8 -*-
"""
Created on Mon May 10 11:16:00 2021

@author: scout
"""

''' the towers of hanoi is  a problem where there are 3 pillars. one of the pillars has n disks on it, each with a unique size, going from smallest on
top to largest on bottom. You must move all of the disks to a new tower. you may move 1 disck at a time, and you cannot place a larger disk on top
of a smaller disk. it should return a sequence of moves that gives the solved problem'''

'''A tower is a dictionary, as follows: {“name”: “A”, “discs”: [1,2,3]}'''

'''It should return the sequence of moves, where each move is a tuple of (disc, from-tower, to-tower), for example (2, “A”, “C”) means move the #2 disc 
from A to C.'''


'''the recursive way tp do this is to solve the problem for every ring except the bigest one on the extra tower, move the biggest one to the extra,
then recurse. solve for everything but the new largest (in realisty the 2nd largest), move the new smallest onto the correct ring (on top of the 
largest ring), and recurse). '''
    
''' what you want to do for the recursion is solve for everything but the largest ring for the extra tower, move the largest ring to the target tower
then do the same thing, but this time with the extra tower being the new source and the old source being the new extra. keep going until you only
have one ring left, then just move that onto the target tower'''    


# moves_list = []
# origional_source = True
# def hanoi(source, target, extra):
#     print('source:', source, '\ntarget:', target, '\nextra:', extra)
#     global moves_list
#     global origional_source
#     # first, a base case where you have one disk on source. all you do is move it to the target tower
#     if len(source['discs']) == 1:
#         print('discs len == 1')
#         # moves_list.append((source['discs'][0], source['name'], target['name']))
#         origional_source = not origional_source
#         return(target['discs'][0], source['name'], target['name'])
        
#     # every other recursive call you want to switch the source between the origional source and the origional extra
#     # check to see if this is an og source. if it is, make call hanoi with source excluding largest disk as source, extra as target, and target as 
#     # extra
#     elif origional_source:
#         print('origional source before recursive')
#         origional_source = not origional_source
#         moves_list.append(hanoi({'name':source['name'], 'discs':source['discs'][:-1]}, extra, target))
#         print('origional source after recursive')
        
#     # if it isn't og source, call extra - largest as source, source as target, and target as extra
#     elif not origional_source:
#         print('non origional source before recursive')
#         origional_source = not origional_source
#         moves_list.append(hanoi({'name':extra['name'], 'discs':extra['discs'][:-1, source, target]}))
#         print('non origional source after recursive')
        
        
#     return(moves_list)

# def move_disc(disc, source, target):
#     target['discs'].append(disc)
#     del source['discs'][0]
#     return(source, target)

# move_list = []
# def hanoi(source, target, extra):
#     print('source:', source, '\ntarget:', target, '\nextra:', extra)
#     global move_list
#     if len(source['discs']) == 1:
#         # target['discs'].insert(0,source['discs'][0])
#         # del source['discs'][0]
#         # move_list.append((target['discs'][0], source['name'], target['name']))
#         return((target['discs'][0], source['name'], target['name'])) 
#     else:
#         hanoi({'name':source['name'], 'discs':source['discs'][:-1]}, extra, target)
#         repeats = len(source['discs']) -1
#         for i in range(repeats):
#              del source['discs'][0]
#         target.
#         hanoi(source, target, extra)
#         hanoi(extra, target, source)
#     return(move_list)
        
        
def hanoi(source, target, extra):
    if len(source['discs']) == 1:
        return([(source['discs'][0], source['name'], target['name'])]) 
    else:
        moves_list = hanoi({'name':source['name'], 'discs':source['discs'][:-1]}, extra, target)
        extra['discs'] = source['discs'][:-1]
        moves_list += [(source['discs'][-1], source['name'], target['name'])]
        moves_list += (hanoi(extra, target, source))
    return(moves_list)









