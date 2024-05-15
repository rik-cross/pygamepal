#
# pygamepal, by Rik Cross
#  -- homepage: github.com/rik-cross/pygamepal
#  -- MIT licenced, free to use, modify and distribute
#  -- run 'pip install pygamepal' to use
#

import pygame
import random

class Particle():

    def __init__(self, position, velocity, acceleration, lifetime, size, sizeDecay, color):
        self.lifetime = lifetime
        self.position = position
        self.acceleration = acceleration
        self.velocity = velocity
        self.color = color
        self.size = size
        self.sizeDecay = sizeDecay
        self.finished = False

    def update(self, deltaTime=1):
        self.size -= self.sizeDecay * deltaTime
        self.lifetime -= 1
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
        pygame.draw.circle(
            surface,
            self.color,
            self.position,
            self.size)

class Particles():

    def __init__(self,
                 # emitter attributes
                 emitterPosition=(0,0), emitterSize=(0,0),
                 emitterLifetime=100,
                 emitterVelocity=(0,0), emitterAcceleration=(0,0),
                 emitterParticleDelay=5,
                 # particle attributes
                 particleVelocityMin=(-1,-1), particleVelocityMax=(1,1),
                 particleAccelerationMin=(0,0), particleAccelerationMax=(0,0),
                 particleLifetime=100,
                 particleSize=20,
                 particleSizeDecay=0.2,
                 particleColors=None
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

        # default color is white
        if particleColors == None:
            self.particleColors = ['white']
        else:
            self.particleColors = particleColors

        # this is set to true once the emitter lifetime is reached
        self.finished = False
    
    # todo - use deltaTime
    def update(self, deltaTime=1):
        
        if self.finished:
            return
        
        #
        # update this particle emitter
        #

        if self.lifetime > 0:
            self.lifetime -= 1
        
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
                lifetime=self.particleLifetime,
                acceleration=randomAcceleration,
                position=randomPosition,
                velocity= randomVelocity,
                color=random.choice(self.particleColors),
                size=self.particleSize,
                sizeDecay=self.sizeDecay
            ))

        # update each particle
        for p in self.particleList:
            p.update(deltaTime)
            if p.size <= 0 or p.lifetime <= 0:
                self.particleList.remove(p)

    def draw(self, surface):

        if self.finished:
            return

        for p in self.particleList:
            p.draw(surface)