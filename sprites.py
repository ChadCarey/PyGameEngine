import pygame
from pygame.sprite import Sprite, Group
from os import path
from Display import Renderable

class EntityBase(Sprite, Renderable):
    
    def __init__(self, imageFilename, maskFilename, resourceLoader):
        Sprite.__init__(self)
        self.resourceLoader = resourceLoader
        self.image = resourceLoader.load_image(imageFilename)
        self.rect = self.image.get_rect()
        # Makes the transparent parts of the Surface not set, and the opaque parts set.
        # The alpha of each pixel is checked to see if it is greater than the given threshold
        self.mask = resourceLoader.load_mask(maskFilename)
        self.x = 10
        self.y = 10


    def render(self, screen):
        screen.blit(self.image, self.rect)
    
    def set_position(self, x, y):
        self.rect = self.rect.move(x,y)
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.set_position(self.x+dx, self.y+dy)

    def updatePhysics(self, timeDelta):
        pass



class Balloon(EntityBase):
    def __init__(self, resourceLoader):
        self.imageFilename = 'ball.png'
        self.maskFilename = 'ball.png'
        EntityBase.__init__(self, self.imageFilename, self.maskFilename, resourceLoader)
