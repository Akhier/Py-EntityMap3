from S_MakeMap import MapGen


gen = MapGen()
gen.debug = True
for seed in range(10):
    gen.create(seed)
print('Done!')
