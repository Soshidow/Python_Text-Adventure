from Classes import *
from Functions import *
# to-do list
    # refactor the ReadMap function so that I can use the object.name property and remove the areaMapKeys.

# SETUP----------------------------------------------------------------------------------------------------------------
# create your objects--------------------------------------------------------------------
player = PlayerCharacter("player", "This is yourself.")

wall = BoundaryObject("wall", "A wall.")

bone = CollectableObject("bone", "A grisly looking bone with teeth marks scoring the surface.")

# read your map--------------------------------------------------------------------------
areaMap = ReadMap("Resources/Map.txt")



# ---------------------------------------------------------------------------------------------------------------------
# GAMEPLAY-------------------------------------------------------------------------------------------------------------

player.Move(areaMap, 0)
player.Move(areaMap, 90)
player.Move(areaMap, 0)
player.Move(areaMap, 180)
player.Move(areaMap, 270)