import pygame

class Camera:

    def __init__(self, position=(0, 0), size=(640, 480),
                 target=(0, 0), zoom=1, backgroundColour='gray30',
                 borderColour='black', borderThickness=2, 
                 clamp=False, clampRect=(0, 0, 1000, 1000),
                 followDelay=0):
        self.position = position
        self.size = size
        # sets the camera center
        self.target = target
        self._currentTarget = self.target
        self._zoom = zoom
        self.backgroundColour = backgroundColour
        self.borderColour = borderColour
        self.borderThickness = borderThickness
        self.clamp = clamp
        self.clampRect = clampRect
        # follow delay: value between 0 (instant snap to target) and 1 (no movement)
        self.followDelay = followDelay

    def update(self, deltaTime=1):
        # update the target using the follow amount
        self._currentTarget = (self._currentTarget[0]*self._followDelay + self.target[0]*(1-self._followDelay),
                         self._currentTarget[1]*self._followDelay + self.target[1]*(1-self._followDelay))

    # draws the surface to the destination surface
    # using the camera attributes
    def draw(self, surface, destSurface):
        # draw border
        pygame.draw.rect(destSurface, self.borderColour, 
                         (self.position[0] - self.borderThickness, self.position[1] - self.borderThickness, 
                          self.size[0] + self.borderThickness*2, self.size[1] + self.borderThickness*2))
        # ensure that the surface is clipped to the camera dimensions
        destSurface.set_clip((self.position[0], self.position[1], self.size[0], self.size[1]))
        # fill the surface to the background color
        destSurface.fill(self.backgroundColour)
        # blit the (zoomed) surface to the destination, and set the target as the center
        x = 0 - (self.size[0]/2 - self._currentTarget[0] * self._zoom)
        y = 0 - (self.size[1]/2 - self._currentTarget[1] * self._zoom)
        # clamp to clampRect coordinates
        if self.clamp:
            x = max(self.clampRect[0] * self.zoom, min(self.clampRect[2] * self.zoom - self.size[0], x))
            y = max(self.clampRect[1] * self.zoom, min(self.clampRect[3] * self.zoom - self.size[1], y))
        # draw the surface to the destination using the correct position, size, center and zoom
        destSurface.blit(pygame.transform.scale(surface, (surface.get_width()*self._zoom, surface.get_height()*self._zoom)), 
                         self.position, 
                         (x, y,
                          self.size[0], self.size[1]))
        # reset surface clipping
        destSurface.set_clip()

    # zoom property, to avoid zoom of < 0.1
    @property
    def zoom(self):
        return self._zoom
    
    @zoom.setter
    def zoom(self, value):
        self._zoom = max(value, 0.1)

    # followAmount property, to clamp value between 0 and 1
    @property
    def followDelay(self):
        return self._followDelay
    
    @followDelay.setter
    def followDelay(self, value):
        self._followDelay = max(0, min(1, value))
