#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
from math import sin
from random import uniform

class Camera:
    
    '''
    A camera can be used to render any source surface to another destination
    surface, using its parameters (size, position, target position, zoom, etc.). `Example code`_.

    .. _Example code: https://github.com/rik-cross/pygamepal/blob/main/examples/cameraExample.py

    .. image:: https://github.com/rik-cross/pygamepal/blob/main/examples/gifs/cameraExample.gif?raw=true

    :param tuple(int, int) position: the top-left (x, y) coordinate for the camera.
    :param tuple(int, int) size: the size (w, h) of the camera (default = (640, 480), or the parent `Scene` size if used within a `Scene`).
    :param tuple(int, int) target: the coordinate (x, y) of the source surface to draw at the center of the camera (default = (0, 0)).
    :param float lazyFollow: the delay when updating the camera target. 0 = instant snap to target, 1 = no movement (default = 0).
    :param float zoom: the amount to scale the source target (default = 1).
    :param float minZoom: the minimum allowed zoom (default = 0.1).
    :param float maxZoom: the maximum allowed zoom (default = 10).
    :param float lazyZoom: the delay when updating the zoom calue. 0 = instant zoom, 1 = no change in zoom (default = 0).
    :param pygame.Color backgroundColor: the background color (default = 'cornflowerblue').
    :param pygame.Color borderColor: the color of the border (default = 'black').
    :param int borderThickness: the thickness of the border(default = 2).
    :param bool clamp: specifies whether the camera should stay within a specific boundary of the source surface (default = False).
    :param tuple(int, int, int, int) clampRect: the boundary (x, y, w, h) of the source surface that the camera should stay within.
    :param float oscillateSpeed: the speed at which the camera should shake (default = 0.2).
    :param int shakeMagnitude: the magnitude of the camera shake (default = 30).
    :param tuple(float, float) shakeDirection: the (x, y) direction of the shake (default = (1, 0)).
    :param float shakeDampening: the reduction in camera shake magnitude each frame (default = 0.4).
    :param float shakeNoise: the amount of random noise to add to the shake (default = 0.8).
    '''

    def __init__(
        self, position = (0, 0),
        size = (640, 480),
        target = (0, 0),
        lazyFollow = 0,
        zoom = 1, minZoom = 0.1, maxZoom = 10,
        lazyZoom = 0,
        backgroundColor = 'cornflowerblue',
        borderColor='black',
        borderThickness = 2,
        clamp = False,
        clampRect = (0, 0, 1000, 1000),
        oscillateSpeed = 0.2,
        shakeMagnitude = 30,
        shakeDirection = (1, 0),
        shakeDampening = 0.4,
        shakeNoise = 0.8
        ):

        self.position = position
        self.size = size

        # sets the camera target info
        self.target = target
        self._currentTarget = self.target
        self._lazyFollow = lazyFollow

        # sets the zoom info
        self.minZoom = minZoom
        self.maxZoom = maxZoom
        self.zoom = zoom
        self._currentZoom = zoom
        self._lazyZoom = lazyZoom
        
        # background
        self.backgroundColor = backgroundColor

        # border
        self.borderColor = borderColor
        self.borderThickness = borderThickness
        
        # clamp
        self.clamp = clamp
        self.clampRect = clampRect

        # screen shake
        self.oscillateSpeed = oscillateSpeed
        self.shakeMagnitude = shakeMagnitude
        self.shakeDirection = shakeDirection
        self.shakeDampening = shakeDampening
        self.shakeNoise = shakeNoise
        self._shakeTime = 0
        self._shakeCurrent = (0, 0)
        self._shakeCurrentMagnitude = 0

    def update(self, deltaTime = 1):

        '''
        Updates the camera target position and, zoom and shake. This method must be called
        each frame if using a camera in isolation, but the method is called automatically
        for cameras with a parent scene.

        :param float deltaTime: the game time elapsed since the last frame (default = 1).
        '''

        #
        # clamp the camera to the clampRect if required
        #

        if self.clamp:
            # clamp x
            if (self.clampRect[2] - self.clampRect[0]) * self._currentZoom > self.size[0]:
                left = ((self.size[0] / 2) / self._currentZoom) + self.clampRect[0]
                right = ((self.size[0] / 2) / self._currentZoom * -1) + self.clampRect[2]
                self.target = (max(left, min(right, self.target[0])),
                               self.target[1])
            else:
                self.target = (self.clampRect[2] / 2, self.target[1])

            # clamp y
            if (self.clampRect[3] - self.clampRect[1]) * self._currentZoom > self.size[1]:
                top = ((self.size[1] / 2) / self._currentZoom) + self.clampRect[1]
                bottom = ((self.size[1] / 2) / self._currentZoom * -1) + self.clampRect[3]
                self.target = (self.target[0],
                               max(top, min(bottom, self.target[1])))
            else:
                self.target = (self.target[0], self.clampRect[3] / 2)
        
        #
        # update the current target using the target and 'lazy follow' values
        #

        self._currentTarget = (self._currentTarget[0] * self._lazyFollow + self.target[0] * (1 - self._lazyFollow),
                               self._currentTarget[1] * self._lazyFollow + self.target[1] * (1 - self._lazyFollow))
        
        #
        # update screen shake
        #

        # oscillate in a sin wave over time, based on the oscillate speed
        self._shakeTime += deltaTime * self.oscillateSpeed
        shakeOffset = (sin(self._shakeTime), sin(self._shakeTime))
        # add some randomness, based on the noise
        dx = uniform(-1, 1) * self.shakeNoise
        dy = uniform(-1, 1) * self.shakeNoise
        shakeOffset = (shakeOffset[0] + dx, shakeOffset[1] + dy)
        # clamp the offset to the maximum shake offset
        shakeOffset = (max(-1, min(1, shakeOffset[0])), max(-1, min(1, shakeOffset[1])))
        self._shakeCurrent = (shakeOffset[0] * self._shakeCurrentMagnitude * self.shakeDirection[0],
                              shakeOffset[1] * self._shakeCurrentMagnitude * self.shakeDirection[1])
        # reduce the shake magnitude by the dampening amount
        self._shakeCurrentMagnitude = max(0, self._shakeCurrentMagnitude - self.shakeDampening)
        # reset the shake time once the shake is complete
        if self._shakeCurrentMagnitude == 0:
            self._shakeTime = 0

        # update the current zoom amount using the target and 'lazy zoom' values
        self._currentZoom = self._currentZoom * self._lazyZoom + self.zoom * (1 - self._lazyZoom)
                                  
    # draws the surface to the destination surface
    # using the camera's attributes
    def draw(self, surface, destSurface):

        '''
        Draws the source surface to the destination surface, using the camera parameters.
        This method must be called each frame if using a camera in isolation, but the method
        is called automatically for cameras with a parent scene.

        :param pygame.Surface surface: the surface to draw.
        :param pygame.Surface destSurface: the surface to draw to.
        '''

        # draw border
        pygame.draw.rect(destSurface, self.borderColor, 
                         (self.position[0] - self.borderThickness, self.position[1] - self.borderThickness, 
                          self.size[0] + self.borderThickness * 2, self.size[1] + self.borderThickness * 2), self.borderThickness, border_radius = 1)
        # ensure that the surface is clipped to the camera dimensions
        destSurface.set_clip((self.position[0], self.position[1], self.size[0], self.size[1]))
        # fill the surface to the background color
        destSurface.fill(self.backgroundColor)

        # blit the (zoomed) surface to the destination, and set the target as the center
        x = 0 - (self.size[0] / 2 - self._currentTarget[0] * self._currentZoom)
        y = 0 - (self.size[1] / 2 - self._currentTarget[1] * self._currentZoom)
        # add screen shake
        x += self._shakeCurrent[0]
        y += self._shakeCurrent[1]

        # draw the surface to the destination using the correct position, size, center and zoom
        destSurface.blit(pygame.transform.scale(surface, (surface.get_width() * self._currentZoom, surface.get_height() * self._currentZoom)), 
                         self.position, 
                         (x, y,
                          self.size[0], self.size[1]))
        # reset surface clipping
        destSurface.set_clip()

    def shake(self, direction = None):

        '''
        Start a camera shake.

        :param tuple(float, float) direction: the (x, y) direction of the shake (default = None, use the stored direction).
        '''

        if direction is not None:
            self.shakeDirection = direction
        self._shakeCurrentMagnitude = self.shakeMagnitude
    
    def setTarget(self, value, instant = False):

        '''
        Set the camera target position. This method permits the instant setting of a position.

        :param bool instant: set the position instantly, ignoring the stored 'lazyFollow' value (default = False).
        '''

        self.target = value
        if instant is True:
            self._currentTarget = value

    def setZoom(self, value, instant = False):

        '''
        Set the camera target zoom value. This method permits the instant setting of the zoom.

        :param bool instant: set the zoom value instantly, ignoring the stored 'lazyZoom' value (default = False).
        '''

        self.zoom = value
        if instant is True:
            self._currentZoom = value

    #
    # properties
    #

    # zoom property, clamped between 0 and 1
    @property
    def zoom(self):
        '''
        Get / set the zoom value (between specified 'minZoom' and 'maxZoom' values).
        '''
        return self._zoom
    
    @zoom.setter
    def zoom(self, value):
        self._zoom = max(self.minZoom, min(self.maxZoom, value))    
        
    @property
    def lazyFollow(self):
        '''
        Get / set the lazy follow value, between 0 and 1.
        '''
        return self._lazyFollow
    
    @lazyFollow.setter
    def lazyFollow(self, value):
        self._lazyFollow = max(0, min(1, value))

    @property
    def lazyZoom(self):
        '''
        Get / set the lazy zoom value, between 0 and 1.
        '''
        return self._lazyZoom
    
    @lazyZoom.setter
    def lazyZoom(self, value):
        self._lazyZoom = max(0, min(1, value))