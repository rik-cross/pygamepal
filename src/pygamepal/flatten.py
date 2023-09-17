import pygame

# flatten a 2D or [n]D list into a single list

def flatten(list):
    newList = []
    for i in list:
        for j in i:
            newList.append(j)
    return newList