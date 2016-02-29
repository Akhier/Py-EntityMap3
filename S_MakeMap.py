import random


class MapGen:

    def __init__(self):
        self.roomsize = (3, 9)
        self.hallsize = (1, 3)

    def create(self):
        centerroom = _room(3, 5, 5, (0, 0))
        ring = [centerroom]
        self._process_ring(ring)

    def _process_ring(self, ring):
        newring = []
        while ring:
            for room in ring:
                rdirlst = ['N', 'S', 'E', 'W']
                random.shuffle(rdirlst)
                width = random.randint(self.roomsize[0],
                                       self.roomsize[1])
                height = random.randint(self.roomsize[0],
                                        self.roomsize[1])
                while rdirlst:
                    direction = rdirlst.pop()


class _room:

    def __init__(self, connectionstomake, width, height, center):
        self.connectionstomake = connectionstomake
        self.W = width
        self.H = height
        self.Center = center
