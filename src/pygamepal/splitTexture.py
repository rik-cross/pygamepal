#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

def splitTexture(texture, newTextureSize, rows = 0, columns = 0, clippingRect = None):

    '''
    Split a texture into a 2D list of sub-textures, using the given size.
    (Use pygamepal.flatten() to flatten the list returned into a single list.)

    :param pygame.texture texture: The original texture to split.
    :param (int, int) newTextureSize: The size (w, h) of each of the new textures.
    :param int rows: The number of rows down to split (default = 0, which means split all available rows).
    :param int columns: The number of columns scross to split (default = 0, which means split all available columns).
    :param pygame.Rect clippingRect: The (x, y, w, h) portion of the source image to split (default = None, which uses all of the source image).
    :return list(list(pygame.texture)) newTextures: The 2D list of new textures.
    '''

    # clip the texture if a clipping rectangle is specified
    if clippingRect is not None:
        texture = texture.subsurface(
            max(0, clippingRect[0]),
            max(0, clippingRect[1]),
            min(clippingRect[2], texture.get_width()),
            min(clippingRect[3], texture.get_height())
        )

    # clip the texture if a number of rows and/or columns are specified
    r = texture.get_height()
    if rows > 0:
        r = min(rows * newTextureSize[1], texture.get_height())
    c = texture.get_width()
    if columns > 0:
        c = min(columns * newTextureSize[0], texture.get_width())
    texture = texture.subsurface((0, 0, c, r))

    # the list of textures to return
    newTextures = []

    # use texture.subsurface to loop through the image
    for row in range(0, texture.get_height(), newTextureSize[1]):

        if row + newTextureSize[1] <= texture.get_height():

            newRow = []
            for column in range(0, texture.get_width(), newTextureSize[0]):
                
                if column + newTextureSize[0] <= texture.get_width():

                    # add the cropped texture to the list
                    newRow.append(texture.subsurface(
                        column, row, newTextureSize[0], newTextureSize[1]))
                
            newTextures.append(newRow)
            
    return newTextures