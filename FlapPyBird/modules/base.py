from FlapPyBird.resources.config import *

class Base(object):
    def __init__(self, basex):
        self.basex = basex
        self.baseShift = BASESHIFT[0]
        self.loopIter = 0

    def move(self, birds):
        if (self.loopIter + 1) % 3 == 0:
            for bird in birds:
                bird.next()
        self.loopIter = (self.loopIter + 1) % 30
        self.basex = -((-self.basex + 100) % self.baseShift)
