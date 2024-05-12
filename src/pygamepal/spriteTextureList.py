#
# PygamePal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

class SpriteTextureList():

    '''
    Used for storing a list of textures (and other info)
    for a SpriteImage state.
    '''

    def __init__(self):
        self._textures = []
        self._animationDelay = 12
        self._loop = True
        self._hFlip = False
        self._vFlip = False
        self._offset = (0, 0)