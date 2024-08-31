#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame

class Particle():

    '''
    A single particle created by a particle emitter.
    (There is no need to use this class directly, as particle emitters create particles themselves.)
    
    :param (int, int) position: The top-left (x, y) position of the particle.
    :param (float, float) velocity: The (x, y) velocity vector, with (0, 0) being stationary.
    :param (float, float) acceleration: The (x, y) acceleration vector, with (0, 0) = no acceleration.
    :param int lifetime: The time after which the particle is deleted.
    :param int size: The radius of the particle.
    :param float sizeDecay: The amount to decrement the size each frame.
    :param pygame.Color color: The particle color.
    '''

    def __init__(self, position, velocity, acceleration, lifetime, size, sizeDecay, color):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.lifetime = lifetime
        self.size = size
        self.sizeDecay = sizeDecay
        self.color = color

        self.finished = False

    def update(self, deltaTime=1):

        '''
        Update method called once per frame by the owner particle emitter.

        :param float deltaTime: The time since the last update (default = 1).
        '''
        
        self.size -= self.sizeDecay * deltaTime
        self.lifetime -= deltaTime
        # update velocity with respect to acceleration
        self.velocity = (
            (self.velocity[0] + self.acceleration[0] * deltaTime),
            (self.velocity[1] + self.acceleration[1] * deltaTime) 
        )
        # update position with respect to velocity
        self.position = (
            self.position[0] + self.velocity[0] * deltaTime,
            self.position[1] + self.velocity[1] * deltaTime 
        )

    def draw(self, surface):

        '''
        Draw method called by the owner particle emitter.

        :param pygame.Surface surface: The surface to draw to.
        '''
        
        pygame.draw.circle(
            surface,
            self.color,
            self.position,
            self.size)