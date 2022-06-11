objectsDict = {}

class Object:
    def __init__(self, name, description):
        self.name = name
        objectsDict[self.name] = self
        self.description = description

    def GetCurrentPosition(self, areaMap):
        for coordinate in areaMap:
            if self in areaMap[coordinate]:
                return coordinate

class BoundaryObject(Object):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.isObstruction = True

class MoveableObject(Object):

    def GetTargetPosition(self, areaMap, angleFromNorth):
        currentPosition = self.GetCurrentPosition(areaMap)

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

    def Move(self, areaMap, angleFromNorth):
        currentPosition = self.GetCurrentPosition(areaMap)
        targetPosition = self.GetTargetPosition(areaMap, angleFromNorth)

        if targetPosition in areaMap: # check if targetPosition exists
            for object in areaMap[targetPosition]:
                if hasattr(object, 'isObstruction') and object.isObstruction:
                    if self.name == 'player':
                        print(f"A {object.name} blocks your path.\n")
                    else:
                        print(f"The {self.name} is blocked by a {object.name}")
                    return False # obstructions block movement, return False

            areaMap[targetPosition].append(self)
        else:
            areaMap[targetPosition] = [self]
        areaMap[currentPosition].remove(self)
        return True # if no obstructions, move into targetPosition and out of currentPosition



class PlayerCharacter(MoveableObject): # Unique MoveableObject for the player.
    def __init__(self, orientation = 0,):
        super().__init__('player', "")
        self.orientation = orientation
        self.inventory = []

    def __Turn(self, angleToTurn):
        return (angleToTurn + self.orientation)%360

    def Look(self, areaMap, angleToTurn):
        target = MoveableObject.GetTargetPosition(areaMap, self.__Turn(angleToTurn))
        return target

# potentially swap these methods round a bit, it would be nice to be able to Look without Turning, but Turn can involve looking
# this may add complications to move though need to think.


    def Move(self, areaMap, angleToTurn):
        self.orientation = self.__Turn(angleToTurn)
        if MoveableObject.Move(self, areaMap, self.orientation):
            for item in self.inventory:
                item.Move(areaMap, self.orientation)

class CollectableObject(MoveableObject): # MoveableObjects that can be collected by the player (and move with them)

    def PickUp(self, areaMap):
        currentPosition = MoveableObject.GetCurrentPosition(self, areaMap)
        for object in areaMap[currentPosition]:
            if object.name == 'player':
                if self in object.inventory:
                    print(f"You are already holding the {self.name}.")
                    return False
                else:
                    object.inventory.append(self)
                    print(f"You pick up the {self.name}.")
                    return True
        print(f"You need to move closer to the {self.name} to pick it up.")
        return False

    def Drop(self, areaMap):
        currentPosition = MoveableObject.GetCurrentPosition(self, areaMap)
        for object in areaMap[currentPosition]:
            if object.name == 'player':
                if self in object.inventory:
                    object.inventory.remove(self)
                    print(f"You dropped the {self.name}.")
                    return True

        print(f"You are not holding the {self.name}.")
        return False

class KeyObject(CollectableObject):
    def __init__(self, name, description, correspondingLock):
        super().__init__(name, description)
        self.correspondingLock = correspondingLock.name

    def Unlock(self, areaMap, lockedObject):
        playerPosition = objectsDict['player'].GetCurrentPosition(areaMap)
        keyPosition = self.GetCurrentPosition(areaMap)

        if playerPosition == keyPosition:
            lockPosition = objectsDict[lockedObject].GetCurrentPosition(areaMap)
            if abs(abs(lockPosition[0] - keyPosition[0]) + abs(lockPosition[1] - keyPosition[1])) <= 1:
                if lockedObject == self.correspondingLock:
                    objectsDict[lockedObject].isObstruction = False
                    print(f"You unlock the {lockedObject}")
                else:
                    print(f"The {self.name} doesn't work for this {lockedObject}.")
            else:
                print(f"You need to move closer to the {lockedObject} to try it.")
        else:
            print(f"You need to move closer to the {self.name} to use it.")
