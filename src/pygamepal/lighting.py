#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
import os

class Light:

    def __init__(self, position = (0, 0), radius = 100, name=None):
        self.position = list(position)
        self.name = name
        self.on = True
        self.radius = radius
    
    def toggle(self):
        self.on = not self.on
    
    #
    # properties
    #

    # radius property, > 1
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

    def __init__(self, surfaceSize = None, ambientLightLevel = 1):
        self.surface = pygame.Surface(surfaceSize, pygame.SRCALPHA)
        self.surface.fill( 'black' )
        self.lightLevel = ambientLightLevel
        self.lights = []
        self.lightMask = pygame.image.load('../src/pygamepal/lightMask.png')

    def update(self, deltaTime = 1):
        pass

    def draw(self, surface):
        
        self.surface.fill('black')
        for l in [x for x in self.lights if x.on]:
            lightSize = (l.radius * 2, l.radius * 2)
            self.surface.blit(pygame.transform.scale(self.lightMask, lightSize), (l.position[0] - (lightSize[0] / 2), l.position[1] - (lightSize[1] / 2)), special_flags=pygame.BLEND_RGBA_SUB)
        surface.blit(self.surface, (0,0))
        self.surface.set_alpha(255 * (1 - self.lightLevel))

    def addLight(self, light):
        self.lights.append(light)
        
    def setLightLevel(self, lightLevel):
        self.lightLevel = min(max(0, lightLevel), 1)

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