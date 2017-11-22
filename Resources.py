
from os import path, makedirs
import pygame

class ResourceLoader(object):
    def __init__(self, resourceFolder='resources'):
        self.resourceFolder = resourceFolder
        self.imageFolder = path.join(self.resourceFolder, 'images')
        self.maskFolder = path.join(self.resourceFolder, 'masks')

        # create dirs that do not exist
        if not path.exists(self.resourceFolder):
            makedirs(self.resourceFolder)
        if not path.exists(self.imageFolder):
            makedirs(self.imageFolder)
        if not path.exists(self.maskFolder):
            makedirs(self.maskFolder)
        
        # initialize caches
        self._images = {}
        self._masks = {}

    def load_image(self, filename):
        '''
        loads the image only if it has not been loaded already
        '''
        if not self.image_exists(filename):
            throw("Image does not exist in "+self.imageFolder+".")
        filepath = path.join(self.imageFolder, filename)
        if filepath in self._images:
            return self._images[filepath]
        else:
            image = pygame.image.load(filepath)
            image.convert()
            self._images[filepath] = image
            return image


    def load_mask(self, filename):
        if not self.mask_exists(filename):
            throw("Mask does not exist in "+self.maskFolder+".")
        filepath = path.join(self.maskFolder, filename)
        if filepath in self._masks:
            print "found", filepath
            return self._masks[filepath]
        else:
            print "did not find", filepath
            maskImage = pygame.image.load(filepath)
            maskImage.convert()
            mask = self.create_mask(maskImage)
            self._masks[filepath] = mask
            return mask

    def mask_exists(self, filename):
        filepath = path.join(self.maskFolder, filename)
        return path.exists(filepath)
    def image_exists(self, filename):
        filepath = path.join(self.imageFolder, filename)
        return path.exists(filepath)

    def create_mask(self, surface):
        return pygame.mask.from_surface(surface, 127)

    def save_mask(self, mask, filename):
        '''
        saves a mask to the masks folder
        '''
        filepath = path.join(self.maskFolder, filename)
        pygame.image.save(mask, filepath)
