import pygame
from Display import Renderer
from EventHandlers import InputEventHandler, ClockEventHandler
from COLORS import WHITE, BLACK
from pygame import time as pytime
from World import World

class GameEngine(object):
    def __init__(self, DEBUG=False):
        x = pygame.init()

        self.height = 800
        self.width = 600
        self.size = (self.height, self.width)
        self.gameDisplay = pygame.display.set_mode( self.size )

        self.title = "Tester"
        pygame.display.set_caption(self.title)

        self.game_exit = False

        # create event handlers
        self.inputHandler = InputEventHandler(DEBUG)
        self.inputHandler.registerQuit(quit)
        self.clockHandler = ClockEventHandler(DEBUG)

        # create the world handler
        self.world = World()

        # create display
        self.renderer = Renderer(self.height, self.width, BLACK)
        # create the clock
        self.clock = pytime.Clock()

    # event callbacks
    def quit(self, *args):
        self.game_exit = True

    def cleanup(self):
        # cleans everything
        pygame.quit()

    def run(self):
        self.game_exit = False
        while not self.game_exit:
            self.inputHandler.runEvents()
            self.clockHandler.runEvents()
            self.renderer.render()
            # get the amount of time that has passed since the last gameUpdate
            timeDelta = self.clock.tick()
            self.world.update(timeDelta)

        self.cleanup()

if __name__ == '__main__':
    engine = GameEngine(True)

    # register events
    engine.inputHandler.registerKeyDown(pygame.K_ESCAPE, engine.quit)

    from sprites import Group, Balloon
    from Resources import ResourceLoader
    loader = ResourceLoader()
    b1 = Balloon(loader)
    b2 = Balloon(loader)
    
    if pygame.sprite.collide_mask(b1, b2):
        print "the sprites have collided."
    else:
        print "They did not collide"

    engine.renderer.register(b1)


    engine.run()
    quit()
