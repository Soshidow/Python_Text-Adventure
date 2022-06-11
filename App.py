from Classes import *
from Functions import *
# to-do list
    # refactor the ReadMap function so that I can use the object.name property and remove the areaMapKeys.

# SETUP----------------------------------------------------------------------------------------------------------------
# create your objects--------------------------------------------------------------------
player = PlayerCharacter()

wall = BoundaryObject("wall", "A wall.")

door = BoundaryObject("door", "A door.")

key = KeyObject("key", "A key.", door)

bone = CollectableObject("bone", "A grisly looking bone with teeth marks scoring the surface.")

# read your map--------------------------------------------------------------------------
areaMap = ReadMap("Resources/Map.txt")

# ---------------------------------------------------------------------------------------------------------------------
# GAMEPLAY-------------------------------------------------------------------------------------------------------------
player.Move(areaMap,180)
player.Move(areaMap,90)
key.PickUp(areaMap)
player.Move(areaMap,180)
print(f"Player: {player.GetCurrentPosition(areaMap)}   Door: {door.GetCurrentPosition(areaMap)}   Player Inventory: {player.inventory}")
player.Move(areaMap, 90)
key.Unlock(areaMap, "door")
player.Move(areaMap,0)
print(f"Player: {player.GetCurrentPosition(areaMap)}   Door: {door.GetCurrentPosition(areaMap)}   Player Inventory: {player.inventory}")