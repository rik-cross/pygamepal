import pygame

#
# input manager
#

class Input():

    # longPressDuraton: the number of milliseconds/frames a key needs to be held to register a long press
    def __init__(self, longPressDuration=1000):
        self.longPressDuration = longPressDuration
        # set key states
        self.currentKeyStates = pygame.key.get_pressed()
        self.previousKeyStates = pygame.key.get_pressed()
        # set long press durations
        self._durations = [0 for _ in range(len(self.currentKeyStates))]

    def update(self, deltaTime=60):
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

    # must be called once per frame to update sprite
    def update(self):
        # only animate if not paused
        if self.pause:
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
        if self._textureLists[self._currentState] == None:
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
# draw utils
#

# easily draw text

def drawText(screen, text, x, y, font=None, antialias=True, colour=(255, 255, 255), background=None):
    # use 'standard' font if none specified
    if font is None:
        font = pygame.font.SysFont(None, 24)
    # create text surface
    textSurface = font.render(text, antialias, colour, background)
    # draw text to screen
    screen.blit(textSurface, (x, y))
