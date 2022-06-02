objectsDict = {}

class Object:
    def __init__(self, name, description):
        self.name = name
        objectsDict[self.name] = self
        self.description = description

class ImmoveableObject(Object):
    pass

class BoundaryObject(ImmoveableObject):
    def __init__(self, name, description):
        Object.__init__(self, name, description)
        self.isObstruction = True


class MoveableObject(Object):

    def GetCurrentPosition(self, areaMap):
        for coordinate in areaMap:
            if self in areaMap[coordinate]:
                return coordinate

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

        # DEBUGGING START
        print(f"{self.name} is attempting to move")
        print(f"Current {self.name} Position: {currentPosition}\tTarget {self.name} Position: {targetPosition}\n")
        # DEBUGGING END

        if targetPosition in areaMap: # check if targetPosition exists
            for object in areaMap[targetPosition]:
                if hasattr(object, 'isObstruction') and object.isObstruction:
                    if self.name == "player":
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
    def __init__(self, name, description, orientation = 0,):
        Object.__init__(self, name, description)
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

    def PickUp(self):
        pass