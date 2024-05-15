#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

# flatten a 2D or [n]D list into a single list

def flatten(list):
    newList = []
    for i in list:
        for j in i:
            newList.append(j)
    return newList