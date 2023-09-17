# used for storing a list of texture (and other info)
# for a spriteImage state

import pygame

class TextureList():
    def __init__(self):
        self._textures = []
        self._animationDelay = 12
        self._loop = True
        self._hFlip = False
        self._vFlip = False
        self._offset = (0, 0)