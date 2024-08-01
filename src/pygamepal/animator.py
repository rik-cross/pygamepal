#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

from .easingFunctions import easeLinear

class Animation:
    def __init__(self, object, parameter, newValue, increment, easingFunction, t):
        self.object = object
        self.parameter = parameter
        self.initialValue = getattr(self.object, self.parameter)
        self.newValue = newValue
        self.increment = increment
        self.easingFunction = easingFunction
        self.currentPercentage = 0
        self.percentageIncrement = 100 / ((self.newValue - getattr(self.object, self.parameter)) / self.increment)
        self.t = t
        self.complete = False
    
    def update(self, deltaTime=1):
        val = self.initialValue + (deltaTime * ((self.newValue - self.initialValue) / 100 * self.easingFunction(self.currentPercentage)))
        if self.newValue > self.initialValue:
            val = min(max(self.initialValue, val), self.newValue)
        if self.newValue < self.initialValue:
            val = min(max(self.newValue, val), self.initialValue)
        
        setattr(self.object, self.parameter, self.t(val))

        if self.currentPercentage >= 100:
            setattr(self.object, self.parameter, self.newValue)
            self.complete = True
        self.currentPercentage += self.percentageIncrement

class Animator:

    def __init__(self):
        self.animations = []

    def addAnimation(self, object, parameter, newValue, duration, easingFunction=easeLinear, type=float):
        increment = (newValue - getattr(object, parameter)) / duration
        self.animations.append(Animation(object, parameter, newValue, increment, easingFunction, type))

    def update(self, deltaTime = 1):
        for a in self.animations:
            a.update()
            if a.complete:
                self.animations.remove(a)