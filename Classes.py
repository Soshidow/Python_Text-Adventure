objectsDict = {}

class Object: # 'Abstract' superclass for properties inherited by all objects.
    def __init__(self, name, description):
        self.name = name
        objectsDict[self.name] = self
        self.description = description # Description to read when the object is encountered

class ImmoveableObject(Object): # Objects which cannot move belong to, or inherit from, this class
    pass

class BoundaryObject(ImmoveableObject): # ImmoveableObjects that block movement
    def __init__(self, name, description):
        Object.__init__(self, name, description)
        self.isObstruction = True


class MoveableObject(Object): # Objects which can move belong to, or inherit from, this class

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
        print(targetPosition)
        # To move we first check the targetposition.

        if targetPosition in areaMap:
            for object in areaMap[targetPosition]:
                if hasattr(object, 'isObstruction') and object.isObstruction:
                    print(f"A {object.name} blocks your path.")
                    return

            areaMap[targetPosition].append(self)
        else:
            areaMap[targetPosition] = [self]

        areaMap[currentPosition].remove(self)



class PlayerCharacter(MoveableObject): # Unique MoveableObject for the player.
    def __init__(self, name, description, orientation = 0,):
        Object.__init__(self, name, description)
        self.orientation = orientation

    def Turn(self, angleToTurn):
        self.orientation = (angleToTurn + self.orientation)%360

    def Look(self, areaMap, angleToTurn):
        self.Turn(angleToTurn)
        target = MoveableObject.GetTargetPosition(areaMap, self.orientation)
        return target

    def Move(self, areaMap, angleToTurn):
        self.Turn(angleToTurn)
        MoveableObject.Move(self, areaMap, self.orientation)

class CollectableObject(MoveableObject): # MoveableObjects that can be collected by the player (and move with them)
    pass