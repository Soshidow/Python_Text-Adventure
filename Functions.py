
def ReadMap(fileLocation): # creates a dictionary with co-ordinates as keys and references to the objects as values.
    try: mapFile = open(fileLocation) # check the file path first
    except:
        print("map file not found")
        return

    else: # if file found:
        mapArray = []
        xRange = 0
        yRange = 0
        # gather max ranges to make rectangular map
        for line in mapFile:
            mapArray.insert(0, line.strip('\n').split('\t'))
            yRange += 1
            # the number of lines is the max range of y
            if len(mapArray[-1]) > xRange:
                xRange = len(mapArray[-1])
            # the longest line is the max range of x
        mapFile.close()

        mapDict = {}

        for y in range(yRange):
            for x in range(xRange):
                if y < len(mapArray) and x < len(mapArray[y]):
                    mapDict[(x,y)] = [mapArray[y][x]]
                # then add it to the mapDictionary with the key being the corresponding coordinates in a tuple, stored the correct way round (x,y)
                else:
                    mapDict[(x,y)] = []
                # otherwise we simply add it to the dictionary with a blank array
        return mapDict

def TranslateMap(areaMap): # translates the references of objects into readable names, useful for debugging.
    debugMap = {}
    for coordinate in areaMap:
        debugMap[coordinate] = []
        for object in areaMap[coordinate]:
            debugMap[coordinate].append(object.name)
    return debugMap
