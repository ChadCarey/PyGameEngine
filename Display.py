import pygame
import uuid
from abc import ABCMeta, abstractmethod

class Renderable(object):
    __metaclass__ = ABCMeta
    '''
    Abstract class for renderable objects

    Renderable object should render themselves
    when the render() method is called
    '''

    def __init__(self, z_index=0):
        ''' Constructor
        z_index    -- This will be used to sort the renderables
                      list when rendering.  z_index is
                      distance from the "camera."
        '''
        self.z_index = z_index
        self.uuid = uuid.uuid1()
        print self.uuid

    @abstractmethod
    def render(self, screen):
        ''' Function called by the renderer'''
        pass

    def __lt__(self, other):
        return self.z_index < other.z_index

    def __le__(self, other):
        return self.z_index <= other.z_index

    def __eq__(self, other):
        return self.z_index == other.z_index

    def __ne__(self, other):
        return self.z_index != other.z_index

    def __gt__(self, other):
        return self.z_index > other.z_index

    def __ge__(self, other):
        return self.z_index >= other.z_index

# TODO: figure out the difference between pygame.display and pygame.screen
# determine how to pass it in from the base class
class Renderer(object):
    def __init__(self, height, width, background=(0,0,0)):
        # List of registered renderable objects
        # that need to be rendered on every frame
        self.renderables = []
        self.screen = pygame.display.set_mode((height, width))
        self.background = background
    def register(self, renderable):
        if renderable:
            self.renderables.append(renderable)

    def unregister(self, removedRend):
        # NOTE this is done this way because __eq__ has been overiden
        length = len(self.renderables)
        for i in range(0,length):
            if removedRend.uuid == self.renderables[i].uuid:
                self.renderables.pop(i)
                break # we need to stop here so there isn't a buffer overflow

    def render(self):
        ''' Render all registered self.renderables'''

        self.screen.fill(self.background)

        # Sort in ascending order, so higher z_index is on top.
        for renderable in sorted(self.renderables):
            renderable.render(self.screen)

        pygame.display.update()
