#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import random
from .particle import Particle

class ParticleEmitter():

    '''
    A marticle emitter creates particles for the duration of its lifetime, with the properties specified.

    .. image:: https://github.com/rik-cross/pygamepal/blob/main/examples/gifs/particlesExample.gif?raw=true
    
    `Example Particles code`_.

    .. _Example Particles code: https://github.com/rik-cross/pygamepal/blob/main/examples/particlesExample.py
    
    Particle emitter attributes:

    :param (int, int) emitterPosition: The (x, y) top-left position of the emitter (default = (0, 0)).
    :param (int, int) emitterSize: The (w, h) size of the emitter. Particles are created randomly within the emitter bounds (default = (0, 0)).
    :param int emitterLifetime: The emitter only emits particles during its lifetime (-1 = forever, default = 100).
    :param (float, float) emitterVelocity: The (x, y) velocity of the emitter (default = no velocity (0, 0)).
    :param (float, float) emitterAcceleration: The (x, y) acceleration of the emitter (default = no acceleration (0, 0)).
    :param float emitterParticleDelay: The delay between particles emitted (default = 5).

    Particle attributes:

    :param (float, float) particleVelocityMin: The minimum (x, y) velocity of a particle (default = (-1, -1)). Emitted particles are given a random velocity between the minimum and maximum.
    :param (float, float) particleVelocityMax: The maximum (x, y) velocity of a particle (default = (1, 1)). Emitted particles are given a random velocity between the minimum and maximum.
    :param (float, float) particleAccelerationMin: The minimum (x, y) acceleration of a particle (default = (0, 0)). Emitted particles are given a random acceleration between the minimum and maximum.
    :param (float, float) particleAccelerationMax: The maximum (x, y) acceleration of a particle (default = (0, 0)). Emitted particles are given a random acceleration between the minimum and maximum.
    :param int particleLifetime: Each particle is destroyed at the end of its lifetime (default = 100).
    :param int particleSize: The radius of each particle (default = 20).
    :param float particleSizeDecay: The amount to decrement the particle size each frame / per second (default = 0.2).
    :param list(pygame.Color) particleColors: Emitted particles are randomly given a color from the list (default = ['white']).
    '''

    def __init__(self,
        # emitter attributes
        emitterPosition = (0, 0),
        emitterSize = (0, 0),
        emitterLifetime = 100,
        emitterVelocity = (0, 0),
        emitterAcceleration = (0, 0),
        emitterParticleDelay = 5,
        # particle attributes
        particleVelocityMin = (-1, -1),
        particleVelocityMax = (1, 1),
        particleAccelerationMin = (0, 0),
        particleAccelerationMax = (0, 0),
        particleLifetime = 100,
        particleSize = 20,
        particleSizeDecay = 0.2,
        particleColors = ['white']
    ):
        
        self.particleList = []
        
        self.position = emitterPosition
        self.size = emitterSize
        self.lifetime = emitterLifetime
        self.acceleration = emitterAcceleration
        self.velocity = emitterVelocity
        
        self.particleVelocityMin = particleVelocityMin
        self.particleVelocityMax = particleVelocityMax
        self.particleAccelerationMin = particleAccelerationMin
        self.particleAccelerationMax = particleAccelerationMax
        self.particleDelay = emitterParticleDelay

        self.particleLifetime = particleLifetime
        self.particleSize = particleSize
        self.sizeDecay = particleSizeDecay
        self.timeSinceLastParticle = 0
        self.particleColors = particleColors

        # this is set to true once the emitter lifetime is reached
        self.finished = False
    
    def update(self, deltaTime = 1):
        
        '''
        Must be called once per frame to update the particle emitter and its particles.

        :param float deltaTime: The time elapsed since the last update (default = 1).
        '''

        if self.finished:
            return
        
        #
        # update this particle emitter
        #

        if self.lifetime > 0:
            self.lifetime -= deltaTime
        
        # transform
        self.velocity = (self.velocity[0] + self.acceleration[0] * deltaTime,
                         self.velocity[1] + self.acceleration[1] * deltaTime)
        
        self.position = (self.position[0] + self.velocity[0] * deltaTime,
                         self.position[1] + self.velocity[1] * deltaTime)

        #
        # emit more particles
        #

        self.timeSinceLastParticle += 1

        if self.lifetime > -1 and self.lifetime <= 0 and len(self.particleList) == 0:
            self.finished = True

        # create new particles
        if self.timeSinceLastParticle >= self.particleDelay and (self.lifetime == -1 or self.lifetime > 0):

            self.timeSinceLastParticle = 0

            # choose random acceleration, velocity and position between limits
            randomAcceleration = (random.uniform(self.particleAccelerationMin[0], self.particleAccelerationMax[0]),
                                  random.uniform(self.particleAccelerationMin[1], self.particleAccelerationMax[1]))
            randomVelocity = (random.uniform(self.particleVelocityMin[0], self.particleVelocityMax[0]),
                              random.uniform(self.particleVelocityMin[1], self.particleVelocityMax[1]))
            # particle can emit from anywhere within the emitter bounds
            randomPosition = (random.uniform(self.position[0], self.position[0] + self.size[0]),
                              random.uniform(self.position[1], self.position[1] + self.size[1]))
            
            # add new particle to the list
            self.particleList.append(Particle(
                lifetime = self.particleLifetime,
                acceleration = randomAcceleration,
                position = randomPosition,
                velocity = randomVelocity,
                color = random.choice(self.particleColors),
                size = self.particleSize,
                sizeDecay = self.sizeDecay
            ))

        # update each particle
        for p in self.particleList:
            p.update(deltaTime)
            if p.size <= 0 or p.lifetime <= 0:
                self.particleList.remove(p)

    def draw(self, surface):

        '''
        Must be called once per frame to draw the emitter's particles.

        :param pygame.Surface surface: The surface to draw to.
        '''

        if self.finished:
            return

        for p in self.particleList:
            p.draw(surface)