from Classes import objectsDict

def InputCommand():
    inputArray = input("\n").lower().split(" ")
    commandArray = []
    for inputString in inputArray:
        commandString = ""
        for letter in inputString:
            if letter.isalpha():
                commandString += letter
        if commandString:
            commandArray.append(commandString)
    return commandArray

def InterperateObject(commandArray):
    objectList = [x for x in commandArray if x in objectsDict]
    return objectList


def InterperateAction(commandArray):
    pass

def InterperateDirection(commandArray):
    pass

def ValidateCommand(commandArray):
    pass
