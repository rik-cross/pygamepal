import pygame

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
            clamp = False, clampRect = (0, 0, 1000, 1000)
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

    def update(self, deltaTime=1):

        # clamp the camera to the clampRect if required
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

        # update the current target using the target and 'lazy follow' values
        self._currentTarget = (self._currentTarget[0] * self._lazyFollow + self.target[0] * (1 - self._lazyFollow),
                               self._currentTarget[1] * self._lazyFollow + self.target[1] * (1 - self._lazyFollow))
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
        # draw the surface to the destination using the correct position, size, center and zoom
        destSurface.blit(pygame.transform.scale(surface, (surface.get_width() * self._currentZoom, surface.get_height() * self._currentZoom)), 
                         self.position, 
                         (x, y,
                          self.size[0], self.size[1]))
        # reset surface clipping
        destSurface.set_clip()

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