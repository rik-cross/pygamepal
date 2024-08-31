#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

from .easingFunctions import easeLinear

class Animator:

    '''
    Changes any object attribute's numerical value over time.

    .. image:: https://github.com/rik-cross/pygamepal/blob/main/examples/gifs/animatorExample.gif?raw=true

    `Example Animator code`_.

    .. _Example Animator code: https://github.com/rik-cross/pygamepal/blob/main/examples/animatorExample.py
    '''

    def __init__(self):
        self.animations = []

    def addAnimation(self, object, attribute, newValue, duration, easingFunction = easeLinear, type=float):

        '''
        Add a new Animation to the Animator.
        
        :param Object object: The object to animate a value for.
        :param str attribute: A string representation of the attribute to animate.
        :param float newValue: The new end value to animate to.
        :param float duration: The time to animate from the old to new value.
        :param func(x) easingFunction: The easing function for the animnation (default = pygamepal.easeLinear).
        :param type type: Parameter type (avoids type errors (e.g. if set to int), default = float).
        '''

        from .animation import Animation
        # create a new Animation object
        self.animations.append(Animation(object, attribute, newValue, duration, easingFunction, type))

    def update(self, deltaTime = 1):

        '''
        Updating the Animator updates each Animation in the Animator. Must be called once per frame.
        '''

        for a in self.animations:
            # update animation
            a.update(deltaTime)
            # remove if complete
            if a.complete:
                self.animations.remove(a)