import pygame

#
# input manager
#

class Input():

    # number of frames a key needs to be held to register a long press
    longPressDuration = 10

    def __init__(self):
        
        # set key states
        self.currentKeyStates = pygame.key.get_pressed()
        self.previousKeyStates = pygame.key.get_pressed()
        
        # set long press durations
        self.durations = []
        for i in range(len(self.currentKeyStates)):
            self.durations.append(0)

    def update(self):

        # update key presses
        self.previousKeyStates = self.currentKeyStates
        self.currentKeyStates = pygame.key.get_pressed()

        # update press durations
        newDurations = []
        for i in range(len(self.currentKeyStates)):
            if self.currentKeyStates[i] and self.previousKeyStates[i]:
                newDurations.append(self.durations[i]+1)
            else:
                newDurations.append(0)
        self.durations = newDurations
    
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

    # returns true if the key denoted by keyCode
    # is held down for a long press during the current frame
    def isKeyLongDown(self, keyCode):
        return self.durations[keyCode] >= Input.longPressDuration

    # returns true if the key denoted by keyCode
    # has achieved a long press in the current frame
    def isKeyLongPressed(self, keyCode):
        return self.durations[keyCode] == Input.longPressDuration

    # returns keyCode progress towards a long press (0%-100%)    
    def GetLongKeyPressPercentage(self, keyCode):
        return min(100, self.durations[keyCode] / Input.longPressDuration * 100)
    
