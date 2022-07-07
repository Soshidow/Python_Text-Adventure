from FileInterpretation import ReadMap

referenceMap = ReadMap("Resources/Map.txt") # dictionary of coordinate-reference pairs
objectsDict = {} # dictionary of name-reference pairs

class Object:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        objectsDict[self.name] = self

        objectFound = False
        for coordinate in referenceMap:
            if self.name in referenceMap[coordinate]:
                objectFound = True
                referenceMap[coordinate].append(self)
                referenceMap[coordinate].remove(self.name)
        if not objectFound:
            print(f"'{self.name}' was not found on the map.")

    def GetCurrentPosition(self):
        for coordinate in referenceMap:
            if self in referenceMap[coordinate]:
                return coordinate

    def GetObjectDistance(self, firstCoordinate, secondCoordinate):
        distance = abs(firstCoordinate[0] - secondCoordinate[0]) + abs(firstCoordinate[1] - secondCoordinate[1])
        return distance


class BoundaryObject(Object):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.isObstruction = True

class MoveableObject(Object):

    def GetTargetPosition(self, angleFromNorth):
        currentPosition = self.GetCurrentPosition()

        match angleFromNorth: # In degrees purely for readability.
            case 0:
                targetPosition = (currentPosition[0], currentPosition[1] + 1)
            case 90:
                targetPosition = (currentPosition[0] + 1, currentPosition[1])
            case 180:
                targetPosition = (currentPosition[0], currentPosition[1] - 1)
            case 270:
                targetPosition = (currentPosition[0] - 1, currentPosition[1])

        return targetPosition

    def Move(self, angleFromNorth):
        currentPosition = self.GetCurrentPosition()
        targetPosition = self.GetTargetPosition(angleFromNorth)

        if targetPosition in referenceMap: # check if targetPosition exists

            for object in referenceMap[targetPosition]:
                if hasattr(object, 'isObstruction') and object.isObstruction:
                    if self.name == 'player':
                        print(f"A {object.name} blocks your path.\n")
                    else:
                        print(f"The {self.name} is blocked by a {object.name}")
                    return False # obstruction blocks movement, return False

            referenceMap[targetPosition].append(self)
        else:
            referenceMap[targetPosition] = [self]
        referenceMap[currentPosition].remove(self)
        return True # no obstruction, append to or create targetPosition and remove self from currentPosition

class PlayerCharacter(MoveableObject): # Unique MoveableObject for the player.
    def __init__(self, orientation = 0,):
        super().__init__('player', "")
        self.orientation = orientation
        self.inventory = []

    def __Turn(self, angleToTurn):
        return (angleToTurn + self.orientation)%360

    def Look(self, angleToTurn):
        target = self.GetTargetPosition(self.__Turn(angleToTurn))
        return target

    def Move(self, angleToTurn):
        self.orientation = self.__Turn(angleToTurn)
        if MoveableObject.Move(self, self.orientation):
            for item in self.inventory:
                item.Move(self.orientation)

class CollectableObject(MoveableObject): # MoveableObjects that can be collected by the player (and move with them)

    def PickUp(self):
        player = objectsDict['player']
        if player.GetCurrentPosition() == self.GetCurrentPosition():
            if self not in player.inventory:
                player.inventory.append(self)
                print(f"You pick up the {self.name}.")
                return True
            else:
                print(f"You are already holding the {self.name}.")
                return False
        else:
            print(f"You need to move closer to the {self.name} to pick it up.")
            return False

    def Drop(self):
        player = objectsDict['player']
        if self in player.inventory:
            player.inventory.remove(self)
            print(f"You dropped the {self.name}.")
            return True
        else:
            print(f"You are not holding the {self.name}.")
            return False

class KeyObject(CollectableObject):
    def __init__(self, name, description, correspondingLock):
        super().__init__(name, description)
        self.correspondingLock = correspondingLock.name

    def Unlock(self, lockedObject):
        player = objectsDict['player']
        playerPosition = player.GetCurrentPosition()

        if self in player.inventory:
            lockPosition = objectsDict[lockedObject].GetCurrentPosition()
            if self.GetObjectDistance(playerPosition, lockPosition) <= 1:
                if lockedObject == self.correspondingLock:
                    objectsDict[lockedObject].isObstruction = False
                    print(f"You unlock the {lockedObject}")
                else:
                    print(f"The {self.name} doesn't work for this {lockedObject}.")
            else:
                print(f"You need to move closer to the {lockedObject} to try it.")
        else:
            print(f"You need to move closer to the {self.name} to use it.")
