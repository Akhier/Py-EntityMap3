class MapGen:

    def __init__(self):
        self.roomsize = (3, 9)
        self.hallsize = (1, 3)

    def create(self):
        centerroom = _room(3, 5, 5, (0, 0))


class _room:

    def __init__(self, connectionstomake, width, height, center):
        self.connectionstomake = connectionstomake
        self.W = width
        self.H = height
        self.Center = center
