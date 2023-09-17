# returns an array of textures, split from the passed texture (spritesheet)
# (this could be a 2-dimensional array)

import pygame

def splitTexture(texture, newTextureWidth, newTextureHeight):

    # the list of textures to return
    newTextures = []

    # use texture.subsurface to loop through the image
    for row in range(0, texture.get_height(), newTextureHeight):
        newRow = []
        for column in range(0, texture.get_width(), newTextureWidth):
            # add the cropped texture to the list
            newRow.append(texture.subsurface(
                column, row, newTextureWidth, newTextureHeight))
        newTextures.append(newRow)

    return newTextures
