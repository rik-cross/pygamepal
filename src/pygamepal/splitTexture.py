#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

def splitTexture(texture, newTextureSize):

    '''
    Split a texture into a 2D list of sub-textures, using the given size.
    (Use pygamepal.flatten() to flatten the list returned into a single list.)

    :param pygame.texture texture: The original texture to split.
    :param (int, int) newTextureSize: The size (w, h) of each of the new textures.
    :return list(list(pygame.texture)) newTextures: The 2D list of new textures.
    '''

    # the list of textures to return
    newTextures = []

    # use texture.subsurface to loop through the image
    for row in range(0, texture.get_height(), newTextureSize[1]):
        newRow = []
        for column in range(0, texture.get_width(), newTextureSize[0]):
            # add the cropped texture to the list
            newRow.append(texture.subsurface(
                column, row, newTextureSize[0], newTextureSize[1]))
        newTextures.append(newRow)

    return newTextures