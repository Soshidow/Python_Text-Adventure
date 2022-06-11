from Classes import objectsDict

def ReadMap(fileLocation): # creates a dictionary with co-ordinates as keys and references to the objects as values.
    try: mapFile = open(fileLocation) # check the file path first
    except:
        print("map file not found")
        return

    else: # if file found:
        mapArray = []
        xRange = 0
        yRange = 0
        # gather the max ranges to make a rectangular map of co-ordinates
        for line in mapFile:
            mapArray.append(line.strip('\n').split('\t'))
            # split lines on tabs and ignore newline characters at the end.
            yRange += 1
            # the number of lines is the max range of y
            if len(mapArray[-1]) > xRange:
                xRange = len(mapArray[-1])
            # the length of the longest line is the max range of x
        mapFile.close()

        # currently the mapArray will read the map coordinates as [y][x]
        # and the y value is reversed (so 0 is the highest point instead of the lowest)
        # Both of these will be changed purely for readability.

        mapArray.reverse()
        # now the y coordinate have reversed, 0 is now the lowest point

        mapDict = {}
        #
        for y in range(yRange):
            for x in range(xRange):
                if y < len(mapArray) and x < len(mapArray[y]) and mapArray[y][x] in objectsDict:
                    mapDict[(x,y)] = [objectsDict[mapArray[y][x]]]
                # if the coordinate corresponds to a string in the array AND that string is a key within mapKeysDict
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

def InterpretCommand(commandString):
    commandArray = commandString.split().lower()
    objectToCommand = None
    for commandWord in commandArray:
        if commandWord in objectsDict:
            objectToCommand = commandArray.pop(commandArray.index(commandWord))
            break

    for commandWord in commandArray:
        pass # I need to think of a way to interpret the string as functions within the objects