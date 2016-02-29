import random
import math


class MapGen:

    def __init__(self):
        self.roomsize = (3, 9)
        self.roomoffset = (3, 7)
        self.roomcon = {1: 35, 2: 55, 3: 10}
        self.hallsize = (1, 3)
        self.usedtiles = []
        self.rooms = []

    def create(self):
        self.usedtiles = []
        self.rooms = []
        centerroom = _room(3, 5, 5, (0, 0))
        self.rooms.append(centerroom)
        self._set_used_tiles(centerroom)
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
                temp = random.randint(1, 100)
                if temp <= self.roomcon[1]:
                    ctm = 1
                elif temp <= self.roomcon[2]:
                    ctm = 2
                else:
                    ctm = 3
                while rdirlst:
                    direction = rdirlst.pop()
                    no_intersection = True
                    offx = 0
                    offy = 0
                    if direction == 'N':
                        offy = -1 * (offset + int(height / 2) +
                                     int(room.H / 2))
                    elif direction == 'S':
                        offy = offset + int(height / 2) + int(room.H / 2)
                    elif direction == 'E':
                        offx = offset + int(width / 2) + int(room.W / 2)
                    elif direction == 'W':
                        offx = -1 * (offset + int(width / 2) + int(room.W / 2))
                    for y in range(height):
                        for x in range(width):
                            center = (x + offx, y + offy)
                            if center in self.usedtiles:
                                no_intersection = False
                    if no_intersection:
                        centerdist = math.hypot(center[0] - room.X,
                                                center[1] - room.Y)
                        if direction == 'N' or direction == 'S':
                            newhall = _room(0, 1, centerdist[1])
                        room.connectionstomake -= 1
                        newroom = _room(ctm, width, height, center)
                        self._set_used_tiles(newroom)
                        self.rooms.append(newroom)
                        newring.append(newroom)

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
