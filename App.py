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

# ---------------------------------------------------------------------------------------------------------------------
# GAMEPLAY-------------------------------------------------------------------------------------------------------------
player.Move(180)
player.Move(90)
key.PickUp()

player.Move(180)
player.Move(90)
key.Unlock('door')
player.Move(0)
