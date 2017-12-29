import pygame
from pygame.sprite import Sprite, Group
from os import path
from Display import Renderable

class EntityBase(Sprite, Renderable):
    
    def __init__(self, image, mask, z_index=0):
        Sprite.__init__(self)
        self.z_index=z_index
        self.image = image
        self.rect = self.image.get_rect()
        # Makes the transparent parts of the Surface not set, and the opaque parts set.
        # The alpha of each pixel is checked to see if it is greater than the given threshold
        self.mask = mask
        self.rect.x = 10
        self.rect.y = 10

    @property
    def x(self):
        return self.rect.x
    @x.setter
    def x(self, value):
        self.set_position(value, self.y)
    @property
    def y(self):
        return self.rect.y
    @y.setter
    def y(self, value):
        self.set_position(self.x, value)

    def render(self, screen):
        screen.blit(self.image, self.rect)
    
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self, dx, dy):
        self.set_position(self.rect.x+dx, self.rect.y+dy)

    def updatePhysics(self, timeDelta):
        pass
    def updateAI(self, timeDelta):
        pass

