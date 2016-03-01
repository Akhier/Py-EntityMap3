from ComponentManager import ComponentManager
from EntityManager import EntityManager
from C_Tile import Tile
from C_Map import Map
import random
import math
import png


class MapGen:

    def __init__(self):
        self.roomsize = (3, 7)
        self.roomoffset = (1, 5)
        self.width = 60
        self.height = 60
        self.maxdepth = 4
        self.usedtiles = []
        self.rooms = []
        self.debug = False
        self.ccR = 0
        self.ccG = 255
        self.ccB = 255
        self.currentcolor = 0
        self.currentpng = 0

    def color_change(self):
        if self.currentcolor == 0:
            if self.ccR != 0:
                self.ccR = self.ccR - 15
            else:
                if self.ccB != 255:
                    self.ccB = self.ccB + 15
                    if self.ccB == 255:
                        self.currentcolor = 1

                else:
                    self.currentcolor = 1

        elif self.currentcolor == 1:
            if self.ccG != 0:
                self.ccG = self.ccG - 15
            else:
                if self.ccR != 255:
                    self.ccR = self.ccR + 15
                    if self.ccR == 255:
                        self.currentcolor = 2
                else:
                    self.currentcolor = 2

        elif self.currentcolor == 2:
            if self.ccB != 0:
                self.ccB = self.ccB - 15
            else:
                if self.ccG != 255:
                    self.ccG = self.ccG + 15
                    if self.ccG == 255:
                        self.currentcolor = 0

                else:
                    self.currentcolor = 0

    def create(self, seed, maxdepth=3):
        random.seed(seed)
        self.maxdepth = maxdepth
        self.usedtiles = []
        self.rooms = []
        centerroom = _room(3, 5, 5, (int(self.width / 2),
                                     int(self.height / 2)))
        self.rooms.append(centerroom)
        self._set_used_tiles(centerroom)
        ring = [centerroom]
        if self.debug:
            coords = {}
            for value in centerroom.Tiles:
                coords[value] = True
            with open('PNGoutput/' + format(self.currentpng, '04d') +
                      '.png', 'wb') as f:
                w = png.Writer(self.width, self.height, alpha=True)
                templist = []
                for y in range(self.height):
                    innerlist = []
                    for x in range(self.width):
                        innerlist.append(0)
                        innerlist.append(0)
                        innerlist.append(0)
                        innerlist.append(255)
                    templist.append(innerlist)
                w.write(f, templist)
            self.currentpng = self.currentpng + 1
            with open('PNGoutput/' + format(self.currentpng, '04d') +
                      '.png', 'wb') as f:
                w = png.Writer(self.width, self.height, alpha=True)
                templist = []
                for y in range(self.height):
                    innerlist = []
                    for x in range(self.width):
                        if (x, y) in coords:
                            innerlist.append(self.ccR)
                            innerlist.append(self.ccG)
                            innerlist.append(self.ccB)
                            innerlist.append(255)
                        else:
                            innerlist.append(0)
                            innerlist.append(0)
                            innerlist.append(0)
                            innerlist.append(0)
                    templist.append(innerlist)
                w.write(f, templist)
            self.color_change()
            self.currentpng = self.currentpng + 1
        self._process_ring(ring, 0)
        newmap = Map(self.width, self.height, seed)
        tilearray = [[False for y in range(self.height)]
                     for x in range(self.width)]
        for room in self.rooms:
            for tile in room.Tiles:
                tilearray[tile[0]][tile[1]] = Tile(tile[0], tile[1],
                                                   'Stone Floor', '.',
                                                   True, True)
        for y in range(self.height):
            for x in range(self.width):
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
        print('starting depth ' + str(depth) + ' ring len ' + str(len(ring)))
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
                    center = (room.X + offx, room.Y + offy)
                    newroom = _room(3, width, height, center)
                    for tile in newroom.Tiles:
                        if tile in self.usedtiles:
                            no_intersection = False
                        if tile[0] < 1 or tile[0] >= self.width - 1 or \
                                tile[1] < 1 or tile[1] >= self.height - 1:
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
                        self._set_used_tiles(newroom)
                        self._set_used_tiles(newhall)
                        self.rooms.append(newroom)
                        newring.append(newroom)
                        if self.debug:
                            coords = {}
                            for value in newhall.Tiles:
                                coords[value] = True
                            with open('PNGoutput/' +
                                      format(self.currentpng, '04d') +
                                      '.png', 'wb') as f:
                                w = png.Writer(self.width, self.height,
                                               alpha=True)
                                templist = []
                                for y in range(self.height):
                                    innerlist = []
                                    for x in range(self.width):
                                        if (x, y) in coords:
                                            innerlist.append(self.ccR)
                                            innerlist.append(self.ccG)
                                            innerlist.append(self.ccB)
                                            innerlist.append(255)
                                        else:
                                            innerlist.append(0)
                                            innerlist.append(0)
                                            innerlist.append(0)
                                            innerlist.append(0)
                                    templist.append(innerlist)
                                w.write(f, templist)
                            self.color_change()
                            self.currentpng = self.currentpng + 1
                            coords = {}
                            for value in newroom.Tiles:
                                coords[value] = True
                            with open('PNGoutput/' +
                                      format(self.currentpng, '04d') +
                                      '.png', 'wb') as f:
                                w = png.Writer(self.width, self.height,
                                               alpha=True)
                                templist = []
                                for y in range(self.height):
                                    innerlist = []
                                    for x in range(self.width):
                                        if (x, y) in coords:
                                            innerlist.append(self.ccR)
                                            innerlist.append(self.ccG)
                                            innerlist.append(self.ccB)
                                            innerlist.append(255)
                                        else:
                                            innerlist.append(0)
                                            innerlist.append(0)
                                            innerlist.append(0)
                                            innerlist.append(0)
                                    templist.append(innerlist)
                                w.write(f, templist)
                            self.color_change()
                            self.currentpng = self.currentpng + 1
                        break
                room.connectionstomake -= 1
                if room.connectionstomake <= 0:
                    ring.remove(room)
        if depth < self.maxdepth:
            depth += 1
            self._process_ring(newring, depth)

    def _set_used_tiles(self, room):
        temproom = _room(0, room.W, room.H, room.Center)
        if random.randint(0, 3):
            self.usedtiles.extend(temproom.Tiles)
        else:
            self.usedtiles.extend(room.Tiles)


class _room:

    def __init__(self, connectionstomake, width, height, center):
        self.connectionstomake = connectionstomake
        self.W = width
        self.H = height
        self.Center = center
        self.Tiles = []
        for y in range(self.H):
            for x in range(self.W):
                self.Tiles.append((x + self.Center[0] - int(self.W / 2),
                                   y + self.Center[1] - int(self.H / 2)))

    @property
    def X(self):
        return self.Center[0]

    @property
    def Y(self):
        return self.Center[1]

    @property
    def print_full(self):
        return ('CTM:' + str(self.connectionstomake) + ' W:' + str(self.W) +
                ' H:' + str(self.H) + ' Center:' + str(self.Center))
