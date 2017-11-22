

class World(object):
    def __init__(self):
        self.entities = []
    def update(self, timeDelta):
        for up in self.entities:
            up.updatePhysics(timeDelta)
            up.updateAI(timeDelta)
        self.checkCollisions()
    def checkCollisions(self):
        pass
    def addPhysics(self, updatable):
        self.entities.append(updatable)
    def removePhysics(self, updatable):
        self.entities.remove(updatable)
