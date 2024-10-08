#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

class Input():

    '''
    Handle Pygame input more easily, including key/mouse press, release, long-press and double-press.

    `Example Key Input code`_.

    .. _Example Key Input code: https://github.com/rik-cross/pygamepal/blob/main/examples/keyInputExample.py

    `Example Mouse Input code`_.

    .. _Example Mouse Input code: https://github.com/rik-cross/pygamepal/blob/main/examples/mouseInputExample.py
        
    :param int longPressDuration: The number of milliseconds/frames a key needs to be held to register a long press (default = 60).
    :param int mouseDoublePressTimeout: The maximum number of frames between mouse button presses to register a double-press (default = 30).
    '''

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

        '''
        Call once per frame to update.
        (Note: only needs to be called if using independently (i.e. not as part of a game).)

        :param float deltaTime: Time elapsed since last frame (default = 1).
        '''

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

    def isKeyDown(self, keyCode):

        '''
        Returns true if the key denoted by keyCode is held down during the current frame.

        :param pygame.Key keyCode: The key to check.
        '''
        
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == True

    def isKeyPressed(self, keyCode):

        '''
        Returns true if the key denoted by keyCode has been pressed down during the current frame.

        :param pygame.Key keyCode: The key to check.
        '''
        
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == True and self.previousKeyStates[keyCode] == False

    def isKeyDoublePressed(self, keyCode):

        '''
        Returns true if the key denoted by keyCode has been double-pressed during the current frame.

        :param pygame.Key keyCode: The key to check.
        '''
        
        return self._keyPressStates[keyCode] == "double"
    
    def isKeyReleased(self, keyCode):

        '''
        Returns true if the key denoted by keyCode has been released during the current frame.

        :param pygame.Key keyCode: The key to check.
        '''
        
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        return self.currentKeyStates[keyCode] == False and self.previousKeyStates[keyCode] == True

    def getKeyDownDuration(self, keyCode):

        '''
        Returns the number of frames a keyCode has been held down.

        :param pygame.Key keyCode: The key to check.
        '''
        
        return self._keyPressDurations[keyCode]

    def isKeyLongDown(self, keyCode):

        '''
        Returns true if the key denoted by keyCode is held down for a long press during the current frame.

        :param pygame.Key keyCode: The key to check.
        '''
        
        return self._keyPressDurations[keyCode] >= self.longPressDuration

    def isKeyLongPressed(self, keyCode):

        '''
        Returns true if the key denoted by keyCode has achieved a long press in the current frame.

        :param pygame.Key keyCode: The key to check.
        '''
        
        return self._keyPressDurations[keyCode] == self.longPressDuration

    def getKeyLongPressPercentage(self, keyCode):

        '''
        Returns keyCode progress towards a long press (0%-100%).

        :param pygame.Key keyCode: The key to check.
        '''
        
        return min(100, self._keyPressDurations[keyCode] / self.longPressDuration * 100)

    #
    # mouse methods
    #

    def getMouseCursorPosition(self):

        '''
        Returns the pygame mouse pointer position.
        '''
        
        return self.currentMousePosition

    def getMouseDirection(self):

        '''
        Returns the (x,y) movement of the mouse.
        e.g:
        - (-1, -1) = North-West movement.
        - (1, 1) = South-East movement.
        '''
        
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

    def isMouseButtonDown(self, mouseButton):

        '''
        Returns true if the mouse button specified is held down during the current frame.

        :param int mouseButton: The mouse button to check.
        '''
        
        if self.currentMouseButtonStates is None or self.previousMouseButtonStates is None:
            return False
        return self.currentMouseButtonStates[mouseButton] == True
    
    def isMouseButtonPressed(self, mouseButton):

        '''
        Returns true if the mouse button specified has been pressed in the current frame.

        :param int mouseButton: The mouse button to check.
        '''
        
        if self.currentMouseButtonStates is None or self.previousMouseButtonStates is None:
            return False
        return self.currentMouseButtonStates[mouseButton] == True and self.previousMouseButtonStates[mouseButton] == False

    def isMouseButtonDoublePressed(self, mouseButton):

        '''
        Returns true if the mouse button specified has been double-pressed in the current frame.

        :param int mouseButton: The mouse button to check.
        '''
        
        return self._mousePressStates[mouseButton] == "double"

    def isMouseButtonReleased(self, mouseButton):

        '''
        Returns true if the mouse button specified has been released in the current frame.

        :param int mouseButton: The mouse button to check.
        '''
        
        if self.currentMouseButtonStates is None or self.previousMouseButtonStates is None:
            return False
        return self.currentMouseButtonStates[mouseButton] == False and self.previousMouseButtonStates[mouseButton] == True

    def getMouseButtonDownDuration(self, mouseButton):

        '''
        Returns the number of frames a mouse button has been held down.

        :param int mouseButton: The mouse button to check.
        '''
        
        return self._mouseButtonDurations[mouseButton]

    def isMouseButtonLongDown(self, mouseButton):

        '''
        Returns true if the mouse button specified is held down for a long press during the current frame.

        :param int mouseButton: The mouse button to check.
        '''
        
        return self._mouseButtonDurations[mouseButton] >= self.longPressDuration

    def isMouseButtonLongPressed(self, mouseButton):

        '''
        Returns true if the mouse button specified has achieved a long press in the current frame.

        :param int mouseButton: The mouse button to check.
        '''
        
        return self._mouseButtonDurations[mouseButton] == self.longPressDuration

    def getMouseButtonLongPressPercentage(self, mouseButton):

        '''
        Returns mouse button progress towards a long press (0%-100%).

        :param int mouseButton: The mouse button to check.
        '''
        
        return min(100, self._mouseButtonDurations[mouseButton] / self.longPressDuration * 100)
