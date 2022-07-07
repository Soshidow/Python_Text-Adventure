


def TranslateMap(areaMap): # translates the references of objects into readable names, useful for debugging.
    debugMap = {}
    for coordinate in areaMap:
        debugMap[coordinate] = []
        for object in areaMap[coordinate]:
            debugMap[coordinate].append(object.name)
    return debugMap
