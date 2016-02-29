class MapGen:

    def __init__(self):
        self.roomsize = (3, 9)
        self.hallsize = (1, 3)

    def create(self):
        centerroom = createroom(3, 5, 5, (0, 0))
