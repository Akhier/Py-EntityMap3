class Tile:

    def __init__(self, x, y, name, char, passable, seethrough):
        self.X = x
        self.Y = y
        self.TileName = name
        self.Char = char
        self.Passable = passable
        self.Seethrough = seethrough
        self.Name = 'Tile'

    @property
    def coord(self):
        return (self.X, self.Y)
