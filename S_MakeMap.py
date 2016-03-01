from ComponentManager import ComponentManager
from EntityManager import EntityManager
from C_Tile import Tile
from C_Map import Map
import random
import math


class MapGen:

    def __init__(self):
        self.roomsize = (3, 9)
        self.roomoffset = (3, 7)
        self.roomcon = {1: 35, 2: 55, 3: 10}
        self.hallsize = (1, 3)
        self.maxdepth = 5
        self.usedtiles = []
        self.rooms = []

    def create(self, seed, maxdepth=5):
        random.seed(seed)
        self.maxdepth = maxdepth
        self.usedtiles = []
        self.rooms = []
        centerroom = _room(3, 5, 5, (0, 0))
        self.rooms.append(centerroom)
        self._set_used_tiles(centerroom)
        ring = [centerroom]
        self._process_ring(ring, 0)
        NY = 0
        SY = 0
        EX = 0
        WX = 0
        for room in self.rooms:
            if room.Y < NY:
                NY = room.Y
            if room.Y > SY:
                SY = room.Y
            if room.X > EX:
                EX = room.X
            if room.X < WX:
                WX = room.X
        width = int(math.hypot(EX - WX, 0))
        height = int(math.hypot(0, SY - NY))
        newmap = Map(width, height, seed)
        tilearray = [[False for x in range(width)] for y in range(height)]
        for room in self.rooms:
            for y in range(room.H):
                for x in range(room.W):
                    tilex = x - int(room.H / 2)
                    tiley = y - int(room.Y / 2)
                    tilearray[tilex][tiley] = Tile(x, y, 'Stone Floor',
                                                   '.', True, True)
        for y in range(height):
            for x in range(width):
                if not tilearray[x][y]:
                    tilearray[x][y] = Tile(x, y, 'Stone Wall',
                                           '#', False, False)
                newtileid = EntityManager.new_Id()
                ComponentManager.add_Component(newtileid, 'Tile',
                                               tilearray[x][y])
                tilearray[x][y] = newtileid
        newmap.TileIds = tilearray
        newmapid = EntityManager.new_Id()
        ComponentManager.add_Component(newmapid, 'Map', newmap)
        return newmapid

    def _process_ring(self, ring, depth):
        print('starting depth ' + str(depth))
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
                        cx = int(math.hypot(center[0] - room.X, 0))
                        cy = int(math.hypot(0, center[1] - room.Y))
                        centerdist = (cx, cy)
                        if direction == 'N' or direction == 'S':
                            hallC = (room.X, int((room.Y + center[1]) / 2))
                            newhall = _room(0, 1, centerdist[1], hallC)
                        else:
                            hallC = (int((room.X + center[0]) / 2), room.Y)
                            newhall = _room(0, centerdist[0], 1, hallC)
                        self.rooms.append(newhall)
                        newroom = _room(ctm, width, height, center)
                        self._set_used_tiles(newroom)
                        self.rooms.append(newroom)
                        newring.append(newroom)
                        break
                    room.connectionstomake -= 1
                if room.connectionstomake <= 0:
                    ring.remove(room)
        if depth < self.maxdepth:
            depth += 1
            self._process_ring(newring, depth)

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
