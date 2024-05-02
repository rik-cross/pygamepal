import pygame
from math import sin
from random import uniform

class Camera:

    def __init__(
            self, position = (0, 0), size = (640, 480),
            target = (0, 0),
            # follow delay is a (clamped) value between
            # 0 (instant snap to target) and 1 (no movement)
            lazyFollow = 0,
            # passed value for 'zoom' will be clamped
            # between 'minZoom' and 'maxZoom' values
            zoom = 1, minZoom = 0.1, maxZoom = 10,
            # zoom follow delay is a (clamped) value between
            # 0 (instant zoom) and 1 (no zoom)
            lazyZoom = 0,
            backgroundColour = 'gray30',
            borderColour='black', borderThickness = 2,
            # camera doesn't move outside of the clamp
            clamp = False, clampRect = (0, 0, 1000, 1000),
            # camera shake
            # oscillate speed (0 = no movement, 1 = fast)
            oscillateSpeed = 0.2,
            # amount of movement
            shakeMagnitude = 30,
            # movement vector
            shakeDirection = (1, 0),
            # shake dampening (0 = none, 1 = lots)
            shakeDampening = 0.4,
            # shake noise (0 = none, 10 = lots)
            shakeNoise = 0.8,
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
        self.backgroundColour = backgroundColour

        # border
        self.borderColour = borderColour
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

    def update(self, deltaTime=1):

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

        # draw border
        pygame.draw.rect(destSurface, self.borderColour, 
                         (self.position[0] - self.borderThickness, self.position[1] - self.borderThickness, 
                          self.size[0] + self.borderThickness * 2, self.size[1] + self.borderThickness * 2), self.borderThickness, border_radius = 1)
        # ensure that the surface is clipped to the camera dimensions
        destSurface.set_clip((self.position[0], self.position[1], self.size[0], self.size[1]))
        # fill the surface to the background color
        destSurface.fill(self.backgroundColour)
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
        if direction is not None:
            self.shakeDirection = direction
        self._shakeCurrentMagnitude = self.shakeMagnitude

    #
    # properties
    #

    # zoom property, clamped between minZoom and maxZoom
    @property
    def zoom(self):
        return self._zoom
    
    @zoom.setter
    def zoom(self, value):
        self._zoom = max(min(value, self.maxZoom), self.minZoom)

    # lazyZoom property, clamped between 0 and 1
    @property
    def lazyZoom(self):
        return self._lazyZoom
    
    @lazyZoom.setter
    def lazyZoom(self, value):
        self._lazyZoom = max(0, min(1, value))

    # lazyFollow property, clamped between 0 and 1
    @property
    def lazyFollow(self):
        return self._lazyFollow
    
    @lazyFollow.setter
    def lazyFollow(self, value):
        self._lazyFollow = max(0, min(1, value))