def random_map(*arg):
    valorant_maps = [
        'haven',
        'ascent',
        'icebox',
        'bind',
        'breeze',
        'split'
    ]
    if not all(arg):
        for mapBans in arg[1:]:
            # print(mapBans.casefold())
            indextoBan = valorant_maps.index(mapBans.casefold())
            valorant_maps.pop(indextoBan)
            print(valorant_maps)
    else:
        print(valorant_maps)



random_map()
