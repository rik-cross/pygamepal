import pygame

class Game:

    def __init__(self, size = (640, 480), caption = '', fps = 60, fullscreen = False):
       
        pygame.init()
        self.size = size
        self.caption = caption
        self.fps = fps
        self.fullscreen = fullscreen

        self.init()

        # start window in windowed or fullscreen mode
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock() 

        # total elapsed game time
        self.startTime = pygame.time.get_ticks()
        self.gameTime = self.startTime
        self._running = False
        
        # store events so that they aren't 'consumed' by the class
        self.events = []

    def init(self):
        pass

    def _update(self):
        # reset events
        self.events = []
        # respond to quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            else:
                self.events.append(event)
        # calculate delta time
        deltaTime = self.clock.tick(self.fps) / 1000
        # calculate total elapsed time
        self.gameTime = pygame.time.get_ticks() - self.startTime
        # run user update method
        self.update(deltaTime)
        # update clock
        self.clock.tick(self.fps)

    def update(self, deltaTime):
        pass

    def _draw(self):
        self.draw()
        # present the screen
        pygame.display.flip()

    def draw(self):
        pass

    def run(self):
        self._running = True
        while self._running:
            self._update()
            self._draw()
        pygame.quit()

    def quit(self):
        self._running = False

    @property
    def icon(self):
        return self._icon
    
    @icon.setter
    def icon(self, value):
        self._icon = value
        pygame.display.set_icon(self._icon)
