from Classes import *
from CommandInterpretation import *
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
command = InputCommand()
print(InterperateObject(command))