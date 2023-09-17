import pygame

class Game:

    def __init__(self):
        pygame.init()
        self.size = (640, 480)
        self.caption = ''
        self.fps = 60
        self.fullscreen = False
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

    def init(self):
        pass

    def _update(self):
        # respond to quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
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
