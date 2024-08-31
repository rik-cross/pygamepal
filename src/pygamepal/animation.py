#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

class Animation:

    '''
    Creates new animations for the Animator.
    (Users of the PygamePal library should not need to use this class directly. Instead, it is used by pygamepal.Animator).

    :param Object object: The object to animate a value for.
    :param str attribute: A string representation of the attribute to animate.
    :param float newValue: The new end value to animate to.
    :param float duration: The time to animate from the old to new value.
    :param func(x) easingFunction: The easing function for the animnation (default = pygamepal.easeLinear).
    :param type type: Attribute type (avoids type errors (e.g. if set to int), default = float).
    '''

    def __init__(self, object, attribute, newValue, duration, easingFunction, type):
        
        self.object = object
        self.attribute = attribute
        self.initialValue = getattr(self.object, self.attribute)
        self.newValue = newValue
        self.easingFunction = easingFunction
        self.type = type

        # calculate increment per unit of duration
        increment = (self.newValue - self.initialValue) / duration
        # calculate the amount to change per percentage of animation
        self.percentageIncrement = 100 / ((self.newValue - self.initialValue) / (increment))

        # track the progress of the animation
        self.currentPercentage = 0
        self.complete = False
    
    def update(self, deltaTime = 1):

        '''
        Update must be called once per frame.
        
        :param float deltaTime: Time elapsed since last frame (default = 1).
        '''

        # increment the value (clamped between initial and new values)
        val = self.initialValue + (deltaTime * ((self.newValue - self.initialValue) / 100 * self.easingFunction(self.currentPercentage)))
        if self.newValue > self.initialValue:
            val = min(max(self.initialValue, val), self.newValue)
        if self.newValue < self.initialValue:
            val = min(max(self.newValue, val), self.initialValue)
        
        # set the attribute to the incremented value
        setattr(self.object, self.attribute, self.type(val))

        # set final value if complete
        if self.currentPercentage >= 100:
            setattr(self.object, self.attribute, self.newValue)
            self.complete = True
        
        # increment the percentage complete, clamped to 100
        self.currentPercentage += min(100, self.percentageIncrement)