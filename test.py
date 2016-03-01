from ComponentManager import ComponentManager
from S_MakeMap import MapGen


gen = MapGen()
gen.debug = True
mapid = gen.create(222)
newmap = ComponentManager.get_Component('Map', mapid)
with open('test.txt', 'w') as w:
    for y in range(newmap.Height):
        s = ''
        for x in range(newmap.Width):
            tile = ComponentManager.get_Component('Tile', newmap.TileIds[x][y])
            s += tile.Char
        s += '\n'
        w.write(s)
for seed in range(5):
    gen.create(seed)
print('Done!')
