import pygame

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
