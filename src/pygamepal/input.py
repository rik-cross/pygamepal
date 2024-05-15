#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

class Input():

    # longPressDuraton: the number of milliseconds/frames a key needs to be held to register a long press
    # mouseDoublePressTimeout: the maximum number of frames between mouse button presses to register a double-press
    def __init__(self, longPressDuration = 60, doublePressTimeout = 30):
        
        self.longPressDuration = longPressDuration
        self.doublePressTimeout = doublePressTimeout

        # set current and previous states
        self.currentKeyStates = pygame.key.get_pressed()
        self.previousKeyStates = pygame.key.get_pressed()
        self.currentMouseButtonStates = pygame.mouse.get_pressed()
        self.previousMouseButtonStates = pygame.mouse.get_pressed()

        # store previous mouse position
        self.currentMousePosition = pygame.mouse.get_pos()
        self.previousMousePosition = pygame.mouse.get_pos()

        # set long press durations
        self._keyPressDurations = [0 for _ in range(len(self.currentKeyStates))]
        self._mouseButtonDurations = [0 for _ in range(len(self.currentMouseButtonStates))]

        # store info to determine button double-press
        self._keyTimeSinceLastPressed = [0 for _ in range(len(self.currentKeyStates))]
        self._mouseTimeSinceLastPressed = [0 for _ in range(len(self.currentMouseButtonStates))]
        
        # stores the press state of each button
        # 'none' -> 'single' -> 'double'
        self._keyPressStates = ["none" for _ in range(len(self.currentKeyStates))]
        self._mousePressStates = ["none" for _ in range(len(self.currentMouseButtonStates))]

    def update(self, deltaTime = 1):

        #
        # update key press info
        #

        # update key presses
        self.previousKeyStates = self.currentKeyStates
        self.currentKeyStates = pygame.key.get_pressed()

        # update key press durations
        for i in range(len(self._keyPressDurations)):
            if self.currentKeyStates[i]:
                self._keyPressDurations[i] += deltaTime
            else:
                self._keyPressDurations[i] = 0

        # update mouse button time sinse last pressed
        for i in range(len(self._keyTimeSinceLastPressed)):
            if self.isKeyPressed(i) == True :
                self._keyTimeSinceLastPressed[i] = 0
            else:
                self._keyTimeSinceLastPressed[i] += deltaTime

        # update mouse button press state between
        # 'none', 'single' and 'double'
        for i in range(len(self._keyPressStates)):
            # none -> single
            if self._keyPressStates[i] == "none" and self.isKeyPressed(i):
                self._keyPressStates[i] = "single"
            # single -> double
            elif self._keyPressStates[i] == "single" and self.isKeyPressed(i):
                self._keyPressStates[i] = "double"
            # single -> none
            elif self._keyPressStates[i] == "single" and self._keyTimeSinceLastPressed[i] > self.doublePressTimeout:
                self._keyPressStates[i] = "none"
            # double -> none
            elif self._keyPressStates[i] == "double":
                self._keyPressStates[i] = "none"

        #
        # update mouse button info
        #

        # update mouse presses
        self.previousMouseButtonStates = self.currentMouseButtonStates
        self.currentMouseButtonStates = pygame.mouse.get_pressed()

        # update mouse position
        self.previousMousePosition = self.currentMousePosition
        self.currentMousePosition = pygame.mouse.get_pos()
        
        # update mouse button press durations
        for i in range(len(self._mouseButtonDurations)):
            if self.currentMouseButtonStates[i]:
                self._mouseButtonDurations[i] += deltaTime
            else:
                self._mouseButtonDurations[i] = 0
        
        # update mouse button time sinse last pressed
        for i in range(len(self._mouseTimeSinceLastPressed)):
            if self.isMouseButtonPressed(i) == True :
                self._mouseTimeSinceLastPressed[i] = 0
            else:
                self._mouseTimeSinceLastPressed[i] += deltaTime

        # update mouse button press state between
        # 'none', 'single' and 'double'
        for i in range(len(self._mousePressStates)):
            # none -> single
            if self._mousePressStates[i] == "none" and self.isMouseButtonPressed(i):
                self._mousePressStates[i] = "single"
            # single -> double
            elif self._mousePressStates[i] == "single" and self.isMouseButtonPressed(i):
                self._mousePressStates[i] = "double"
            # single -> none
            elif self._mousePressStates[i] == "single" and self._mouseTimeSinceLastPressed[i] > self.doublePressTimeout:
                self._mousePressStates[i] = "none"
            # double -> none
            elif self._mousePressStates[i] == "double":
                self._mousePressStates[i] = "none"

    #
    # key methods
    #

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
    # has been double-pressed during the current frame
    def isKeyDoublePressed(self, keyCode):
        return self._keyPressStates[keyCode] == "double"
    
    # returns true if the key denoted by keyCode
    # has been released during the current frame
    def isKeyReleased(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == False and self.previousKeyStates[keyCode] == True

    # returns the number of frames a keyCode has been held down
    def getKeyDownDuration(self, keyCode):
        return self._keyPressDurations[keyCode]

    # returns true if the key denoted by keyCode
    # is held down for a long press during the current frame
    def isKeyLongDown(self, keyCode):
        return self._keyPressDurations[keyCode] >= self.longPressDuration

    # returns true if the key denoted by keyCode
    # has achieved a long press in the current frame
    def isKeyLongPressed(self, keyCode):
        return self._keyPressDurations[keyCode] == self.longPressDuration

    # returns keyCode progress towards a long press (0%-100%)
    def getKeyLongPressPercentage(self, keyCode):
        return min(100, self._keyPressDurations[keyCode] / self.longPressDuration * 100)

    #
    # mouse methods
    #

    # returns the pygame mouse pointer position
    def getMouseCursorPosition(self):
        return self.currentMousePosition

    # returns the (x,y) movement of the mouse
    def getMouseDirection(self):
        direction = (0, 0)
        currentPosition = self.currentMousePosition
        if currentPosition[0] < self.previousMousePosition[0]:
            direction = (-1, direction[1])
        elif currentPosition[0] > self.previousMousePosition[0]:
            direction = (1, direction[1])
        if currentPosition[1] < self.previousMousePosition[1]:
            direction = (direction[0], -1)
        elif currentPosition[1] > self.previousMousePosition[1]:
            direction = (direction[0], 1)
        return direction

    # returns true if the mouse button specified
    # is held down during the current frame
    def isMouseButtonDown(self, mouseButton):
        if self.currentMouseButtonStates is None or self.previousMouseButtonStates is None:
            return False
        return self.currentMouseButtonStates[mouseButton] == True
    
    # returns true if the mouse button specified
    # has been pressed in the current frame
    def isMouseButtonPressed(self, mouseButton):
        if self.currentMouseButtonStates is None or self.previousMouseButtonStates is None:
            return False
        return self.currentMouseButtonStates[mouseButton] == True and self.previousMouseButtonStates[mouseButton] == False

    # returns true if the mouse button specified
    # has been double-pressed in the current frame
    def isMouseButtonDoublePressed(self, mouseButton):
        return self._mousePressStates[mouseButton] == "double"

    # returns true if the mouse button specified
    # has been released in the current frame
    def isMouseButtonReleased(self, mouseButton):
        if self.currentMouseButtonStates is None or self.previousMouseButtonStates is None:
            return False
        return self.currentMouseButtonStates[mouseButton] == False and self.previousMouseButtonStates[mouseButton] == True

    # returns the number of frames a mouse button has been held down
    def getMouseButtonDownDuration(self, mouseButton):
        return self._mouseButtonDurations[mouseButton]

    # returns true if the mouse button specified
    # is held down for a long press during the current frame
    def isMouseButtonLongDown(self, mouseButton):
        return self._mouseButtonDurations[mouseButton] >= self.longPressDuration

    # returns true if the mouse button specified
    # has achieved a long press in the current frame
    def isMouseButtonLongPressed(self, mouseButton):
        return self._mouseButtonDurations[mouseButton] == self.longPressDuration

    # returns mouse button progress towards a long press (0%-100%)
    def getMouseButtonLongPressPercentage(self, mouseButton):
        return min(100, self._mouseButtonDurations[mouseButton] / self.longPressDuration * 100)
