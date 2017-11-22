# InputEventHandler.py: This is the event handler
# Author: Chad Carey,

import pygame

class InputEventHandler(object):

    def __init__(self, DEBUG=False):
        self.DEBUG = DEBUG
        self._quit_handler = None
        self._keyDownMap = {}
        self._keyUpMap = {}

    def _print(self, *args):
        if self.DEBUG:
            s = ''.join([str(a) for a in args])
            print s

    # REGISTERING METHODS

    def registerKeyDown(self, key, method):
        self._print("Registering key: ", key)
        self._keyDownMap[key] = method
    def unregisterKeyDown(self, key):
        if self._keyDownMap.has_key(key):
            del self._keyDownMap[key]

    def registerQuit(self, method):
        self._quit_handler = method
    def unregisterQuit(self, method):
        self._quit_handler = None

    # TOP LEVEL EVENT HANDLERS

    def _quitEvent(self):
        if self._quit_handler is not None:
            self._quit_handler()

    def _keyDownEvent(self, unicode, key, mod):
        if self._keyDownMap.has_key(key):
            self._keyDownMap[key](unicode, mod)

    def _keyUpEvent(self, key, mod):
        if self._keyUpMap.has_key(key):
            self._keyUpMap[key](mod)

    def _videoExposeEvent(self):
        pass

    def _videoResizeEvent(self, size, width, height):
        pass

    def _activeEvent(self, gain, state):
        pass

    def _mouseMotionEvent(self, pos, rel, buttons):
        pass

    def _mouseButtonUpEvent(self, pos, button):
        pass

    def _mouseButtonDownEvent(self, pos, button):
        pass

    # this method will run all the events and call the appropriate function to handle it
    def runEvents(self):
        for event in pygame.event.get():
            self._print('Event: ', event)
            etype = event.type
            if etype == pygame.QUIT:
                self._quitEvent()
            elif etype == pygame.KEYDOWN:
                self._keyDownEvent(event.unicode, event.key, event.mod)
            elif etype == pygame.KEYUP:
                self._keyUpEvent(event.key, event.mod)
            elif etype == pygame.MOUSEMOTION:
                self._mouseMotionEvent(event.pos, event.rel, event.buttons)
            elif etype == pygame.MOUSEBUTTONUP:
                self._mouseButtonUpEvent(event.pos, event.button)
            elif etype == pygame.MOUSEBUTTONDOWN:
                self._mouseButtonDownEvent(event.pos, event.button)
            elif etype == pygame.VIDEORESIZE:
                self._videoResizeEvent(event.size, event.w, event.h)
            elif etype == pygame.ACTIVEEVENT:
                self._activeEvent(event.gain, event.state)
            elif etype == pygame.VIDEOEXPOSE:
                self._videoExposeEvent()
            elif etype == pygame.USEREVENT:
                self._userEvent(event.code)
            # UNIMPLEMENTED EVENTS
            elif etype == pygame.JOYAXISMOTION:
                pass
            elif etype == pygame.JOYBALLMOTION:
                pass
            elif etype == pygame.JOYHATMOTION:
                pass
            elif etype == pygame.JOYBUTTONUP:
                pass
            elif etype == pygame.JOYBUTTONDOWN:
                pass
            else:
                print "WARNING: unknown event type", etype

import time


# TODO: Possibly needs to be done on a separate thread with an event scheduler
class ClockEventHandler(object):
    class Event(object):
        def __init__(self, name, lastUpdateTime, nextUpdateTime, frequencySeconds, method):
            self.name = name
            self.lastUpdateTime = lastUpdateTime
            self.nextUpdateTime = nextUpdateTime
            self.frequencySeconds = frequencySeconds
            self.method = method

    def __init__(self, DEBUG):
        self.events = []
        self.DEBUG = DEBUG

    def _print(self, *args):
        if self.DEBUG:
            s = ''.join([str(a) for a in args])
            print s

    def register(self, name, frequencySeconds, method):
        curTime = time.time()
        nextUpdateTime = curTime+frequencySeconds
        lastUpdateTime = curTime
        self.events.append( self.Event(name, lastUpdateTime, nextUpdateTime, frequencySeconds, method) )

    def runEvents(self):
        curTime = time.time()
        for event in self.events:
            if event.nextUpdateTime <= curTime:
                self._print(curTime-event.nextUpdateTime)
                timeDelta = curTime-event.lastUpdateTime
                event.method(
                    {
                    'lastUpdateTime': event.lastUpdateTime, 
                    'currentTime': curTime, 
                    'updateFrequency': event.frequencySeconds,
                    'timeDelta': timeDelta
                    })
                event.lastUpdateTime = curTime
                event.nextUpdateTime = curTime+event.frequencySeconds
