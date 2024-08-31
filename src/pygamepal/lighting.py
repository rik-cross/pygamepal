#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
import os

class Light:

    '''
    A light to add to the pygamepal.Lighting system.

    .. image:: https://github.com/rik-cross/pygamepal/blob/main/examples/gifs/lightingExample.gif?raw=true
    
    `Example Lighting code`_.

    .. _Example Lighting code: https://github.com/rik-cross/pygamepal/blob/main/examples/lightingExample.py

    :param (int, int) position: Light position on the drawn surface.
    :param int radius: The radius of the light.
    :param str name: Light name (for getting and controlling if required, default = None).
    :param bool on: Light visibility (default = True).
    '''

    def __init__(self, position = (0, 0), radius = 100, name = None, on = True):
        self.position = list(position)
        self.name = name
        self.radius = radius
        self.on = True
    
    def toggle(self):

        '''
        Toggle the light visibility.
        '''
        
        self.on = not self.on
    
    #
    # properties
    #

    @property
    def radius(self):
        '''
        Get / set the radius value (is set to 0 if given negative value).
        '''
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._radius = max(0, value)

class Lighting:

    def __init__(self, surfaceSize, ambientLightLevel = 0):
        # create a new lighting surface in the specified size
        self.surface = pygame.Surface(surfaceSize, pygame.SRCALPHA)
        self.lightLevel = ambientLightLevel
        # TODO ...
        self.lightMask = pygame.image.load('../src/pygamepal/lightMask.png')
        
        self.lights = []
        self.surface.fill( 'black' )

    def update(self, deltaTime = 1):

        '''
        
        '''
        
        pass

    def draw(self, surface):
        
        self.surface.fill('black')
        for l in [x for x in self.lights if x.on]:
            lightSize = (l.radius * 2, l.radius * 2)
            self.surface.blit(pygame.transform.scale(self.lightMask, lightSize), (l.position[0] - (lightSize[0] / 2), l.position[1] - (lightSize[1] / 2)), special_flags=pygame.BLEND_RGBA_SUB)
        surface.blit(self.surface, (0,0))
        self.surface.set_alpha(255 * (1 - self.lightLevel))

    # TODO over time (duration)?
    def setLightLevel(self, lightLevel):
        self.lightLevel = min(max(0, lightLevel), 1)

    def addLight(self, light):
        self.lights.append(light)

    def getLight(self, name):
        for l in self.lights:
            if l.name == name:
                return l
        return None

    #
    # properties
    #

    # ambient light property, between 0 and 1
    @property
    def ambientLightLevel(self):
        '''
        Get / set the ambient light value (which is set between 0 and 1).
        '''
        return self._ambientLightLevel
    
    @ambientLightLevel.setter
    def ambientLightLevel(self, value):
        self._radius = min(max(0, value), 1)