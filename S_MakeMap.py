import random


class MapGen:

    def __init__(self):
        self.roomsize = (3, 9)
        self.roomoffset = (3, 7)
        self.hallsize = (1, 3)
        self.usedtiles = []

    def create(self):
        self.usedtiles = []
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
                offset = random.randint(self.roomoffset[0],
                                        self.roomoffset[1])
                while rdirlst:
                    direction = rdirlst.pop()
                    if self._check_dir(offset, width, height):

    def _set_used_tiles(self, room):
        for y in range(room.H):
            for x in range(room.W):
                tilex = x - int(room.W / 2) + room.X
                tiley = y - int(room.H / 2) + room.Y
                self.usedtiles.append((tilex, tiley))


class _room:

    def __init__(self, connectionstomake, width, height, center):
        self.connectionstomake = connectionstomake
        self.W = width
        self.H = height
        self.Center = center

    @property
    def X(self):
        return self.Center[0]

    @property
    def Y(self):
        return self.Center[1]
