#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

#
# game abstraction
#

class Game:

    def __init__(self):
        pygame.init()
        self.size = (640, 480)
        self.caption = ''
        self.fps = 60
        self.fullscreen = False
        self.init()
        # start window in windowed or fullscreen mode
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock() 
        # total elapsed game time
        self.startTime = pygame.time.get_ticks()
        self.gameTime = self.startTime
        self._running = False

    def init(self):
        pass

    def _update(self):
        # respond to quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
        # calculate delta time
        deltaTime = self.clock.tick(self.fps) / 1000
        # calculate total elapsed time
        self.gameTime = pygame.time.get_ticks() - self.startTime
        # run user update method
        self.update(deltaTime)
        # update clock
        self.clock.tick(self.fps)

    def update(self, deltaTime):
        pass

    def _draw(self):
        self.draw()
        # present the screen
        pygame.display.flip()

    def draw(self):
        pass

    def run(self):
        self._running = True
        while self._running:
            self._update()
            self._draw()
        pygame.quit()

    def quit(self):
        self._running = False

    @property
    def icon(self):
        return self._icon
    
    @icon.setter
    def icon(self, value):
        self._icon = value
        pygame.display.set_icon(self._icon)

#
# input manager
#

class Input():

    # longPressDuraton: the number of milliseconds/frames a key needs to be held to register a long press
    def __init__(self, longPressDuration=60):
        self.longPressDuration = longPressDuration
        # set key states
        self.currentKeyStates = pygame.key.get_pressed()
        self.previousKeyStates = pygame.key.get_pressed()
        # set long press durations
        self._durations = [0 for _ in range(len(self.currentKeyStates))]

    def update(self, deltaTime=1):
        # update key presses
        self.previousKeyStates = self.currentKeyStates
        self.currentKeyStates = pygame.key.get_pressed()
        # update press durations
        for i in range(len(self._durations)):
            if self.currentKeyStates[i]:
                self._durations[i] += deltaTime
            else:
                self._durations[i] = 0

    # key methods

    # returns true if the key denoted by keyCode
    # is held down during the current frame
    def isKeyDown(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == True

    # returns true if the key denoted by keyCode
    # has been pressed down during the current frame
    def isKeyPressed(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == True and self.previousKeyStates[keyCode] == False

    # returns true if the key denoted by keyCode
    # has been released during the current frame
    def isKeyReleased(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == False and self.previousKeyStates[keyCode] == True

    # long key methods

    # returns the number of frames a keyCode has been held down
    def getKeyDownDuration(self, keyCode):
        return self._durations[keyCode]

    # returns true if the key denoted by keyCode
    # is held down for a long press during the current frame
    def isKeyLongDown(self, keyCode):
        return self._durations[keyCode] >= self.longPressDuration

    # returns true if the key denoted by keyCode
    # has achieved a long press in the current frame
    def isKeyLongPressed(self, keyCode):
        return self._durations[keyCode] == self.longPressDuration

    # returns keyCode progress towards a long press (0%-100%)
    def GetKeyLongPressPercentage(self, keyCode):
        return min(100, self._durations[keyCode] / self.longPressDuration * 100)

#
# Sprites and animations
#

# returns an array of textures, split from the passed texture (spritesheet)
# (this could be a 2-dimensional array)

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

# flatten a 2D or [n]D list into a single list

def flatten(list):
    newList = []
    for i in list:
        for j in i:
            newList.append(j)
    return newList

# used for storing a list of texture (and other info)
# for a spriteImage state

class TextureList():
    def __init__(self):
        self._textures = []
        self._animationDelay = 12
        self._loop = True
        self._hFlip = False
        self._vFlip = False
        self._offset = (0, 0)

# allows for one or more tetxures to be associated with a state

class SpriteImage():

    def __init__(self):
        self._reset()

    # set object to initial values
    def _reset(self):
        # maps a state to a list of textures
        self._textureLists = {}
        self._currentState = None
        # keeps track of current animation frame and progress
        self._animationIndex = 0
        self._animationTimer = 0
        self.pause = False

    # add one or more textures, with an associated state
    def addTextures(self, firstTexture, *moreTextures, state=None, animationDelay=12, loop=True, hFlip=False, vFlip=False, offset=(0,0)):
        # allow textures with no attached state (for single-state images/animations)
        if state is None:
            state = 'default'
        # get existing textureList or create a new one
        if state not in self._textureLists:
            textureList = TextureList()
        else:
            textureList = self._sprites[state]
        # add textures to list
        textureList._textures.append(firstTexture)
        for texture in moreTextures:
            textureList._textures.append(texture)
        # add attributes for the current state
        textureList._animationDelay = animationDelay
        textureList._loop = loop
        textureList._hFlip = hFlip
        textureList._vFlip = vFlip
        textureList._offset = offset
        self._textureLists[state] = textureList
        if len(self._textureLists) == 1:
            self._currentState = state

    def getCenter(self):
        if self._currentState is None or self.pause:
            return (0, 0)
        # get the current animation frame
        currentTexture = self._textureLists[self._currentState]._textures[self._animationIndex]
        return (currentTexture.get_width()/2, currentTexture.get_height()/2)

    # must be called once per frame to update sprite
    def update(self):
        # only animate if there's at least one image and it's not paused
        if self._currentState is None or self.pause:
            return
        # increment timer
        self._animationTimer += 1
        # advance animation if timer reaches delay value
        if self._animationTimer >= self._textureLists[self._currentState]._animationDelay:
            self._animationTimer = 0
            self._animationIndex += 1
            if self._animationIndex > len(self._textureLists[self._currentState]._textures) - 1:
                if self._textureLists[self._currentState]._loop:
                    self._animationIndex = 0
                else:
                    self._animationIndex = len(
                        self._textureLists[self._currentState]._textures) - 1

    def setState(self, state):
        # only change state if the new state is different
        if self._currentState == state:
            return
        # set the new state
        self._currentState = state
        # reset index and timer for the new state
        self.resetState()

    def draw(self, screen, x, y):
        # don't draw if there's nothing to draw
        if self._currentState is None or self._textureLists[self._currentState] == None:
            return
        # get the current animation frame
        currentTexture = self._textureLists[self._currentState]._textures[self._animationIndex]
        # draw (optionally flipped) texture
        screen.blit(pygame.transform.flip(currentTexture,
                                          self._textureLists[self._currentState]._hFlip,
                                          self._textureLists[self._currentState]._vFlip),
                    (x - self._textureLists[self._currentState]._offset[0],
                     y - self._textureLists[self._currentState]._offset[1],
                     currentTexture.get_width(),
                     currentTexture.get_height()))
    # puts sprite animation back to start

    def resetState(self):
        self._animationIndex = 0
        self._animationTimer = 0

#
# Camera
#

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

#
# draw utils
#

# easily draw text

def drawText(screen, text, x=0, y=0, font=None, antialias=True, color=(255, 255, 255), background=None):
    # use 'standard' font if none specified
    if font is None:
        font = pygame.font.SysFont(None, 24)
    # create text surface
    textSurface = font.render(text, antialias, color, background)
    # draw text to screen
    screen.blit(textSurface, (x, y))
