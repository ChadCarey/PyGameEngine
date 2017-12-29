
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
            print "Image does not exist in "+path.abspath(self.imageFolder)+"."
            raise 1
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

class SpriteSheet(object):
    def __init__(self, sheet, imageDict, colorkey=False):
        data = self._images_from(sheet, imageDict, colorkey)
        self.__dict__.update(data)

    # Load a specific image from a specific rectangle
    def _image_at(self, sheet, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        # new surface of rectange size
        image = pygame.Surface(rect.size).convert()
        # blit sheet at rect onto new image
        image.blit(sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def _images_at(self, sheet, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self._image_at(sheet, rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def _load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self._images_at(tups, colorkey)
    def _images_from(self, sheet, layout_dict, colorkey=None):
        images = {}
        for k, rect in layout_dict.iteritems():
            images[k] = self._image_at(sheet, rect, colorkey)
        return images
