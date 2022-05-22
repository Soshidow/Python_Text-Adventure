#from time import sleep
# will eventually use this for delays between printing text

#-------------------------------------------------------------------------------------------------
#Methods for Command Interpretation --------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

actions = {
    "basic actions" : {
        "listen" : "listen"
    },
    "directional actions" : {
        "go": "move", "move": "move", "run": "move", "travel": "move", "walk": "move", "advance": "move",
    },
    "interactional actions" : {
        "check" : "examine", "examine": "examine", "feel" : "examine", "look" : "examine", "touch" : "examine",
        "press": "push", "push" : "push",
        "pull" : "pull", 
        "collect" : "collect" , "grab": "collect", "pick": "collect" 
    },
    "directional interactional actions" : {
        "chuck" : "throw" ,"throw": "throw",
        "climb" : "climb", "ascend" : "climb", "descend" : "climb"
    }
}
directions = {
    "forward": "forward", "advance": "forward", "ahead" : "forward",
    "back": "backward", "retreat": "backward", "behind" : "backward",
    "right": "right",
    "left": "left",
    "up": "upward", "ascend" : "upward",
    "down": "downward", "descend" : "downward"
}

# These are two dictionaries are used to give "codewords" to each action/direction. 
# This way the user can enter multiple descriptions for moving such as "walk", "run" or "go" 
# but I only need my methods to interpret one word for movement "move"

def InputCommand(textToPrint = "", objects = {}):
    # it can take text to print out when it asks for user input, it will default to "".
    # it also takes a dictionary of objects, objects would be a context specific and may be a different variable if I had made multiple "levels" or "areas"

    command = input(f"{textToPrint}").lower()

    # I take the user input in lower case to match my lower case actions, directions and objects dictionaries

    commandDict = {
        "action" : None,
        "direction": None,
        "object" : None
    }

    # A dictionary of the command words, ready to be assigned values.

    for subAction in actions:
        if commandDict["action"] == None:
            for action in actions[subAction]:
                if action in command:
                    commandDict["action"] = {"description": action, "code": actions[subAction][action], "type": subAction}
                    break
        else:
            break
    # check all words in the actions dictionary to see if they are in the user input, if so assign it as the "action"

    for direction in directions:
        if direction in command:
            commandDict["direction"] = {"description": direction, "code": directions[direction]}
            break
    # check all words in the directions dictionary to see if they are in the user input, if so assign it as the "direction"

    if objects:
        for object in objects:
            if object in command:
                commandDict["object"] = object
                break
    # check all words in the objects dictionary to see if they are in the user input, if so assign it as the "object"

    return commandDict

def InterpretCommand(command, interactions = {}):
    # this method is passed the commandDict from the InputCommand method 
    # and an interactions dict that lists all interactions in the area.

    outcome = None
    # this is a variable to return if there is a specific outcome

    action = command["action"]
    direction = command["direction"]
    object = command["object"]

    #these variables are assigned just for convenience in the following code

    if action == None:
        if direction:
            if object:
                print(f"Do what '{direction['code']}' with the '{object}'?")
            else:
                print(f"Do what '{direction['code']}'?")
        elif object and not direction:
            print(f"You don't understand what to do with with the {object}?")
        else:
            print("You don't understand the instruction.")
        return

    # if you fail to provide an "action" keyword then this if-else block will attempt to provide clear instructions on what you missed.

    else:
        # the only time action isn't None is if it successfully found a match in the "actions" dictionary

        if action["type"] in interactions:
            if action["type"] == "basic actions" and action["code"] in interactions["basic actions"]:
                outcome = interactions["basic actions"][action["code"]]

            # if it's a basic action it only needs to confirm that the action keyword is in the interactionDict

            elif action["type"] == "directional actions" and action["code"] in interactions["directional actions"]:
                if direction:
                    if direction["code"] in interactions["directional actions"][action["code"]]:
                        outcome = interactions["directional actions"][action["code"]][direction["code"]]
                else:
                    print(f"{action['description']} in what direction?")
                    return

            # if it's a directional action it has to confirm that the action is in the interactionDict
            # and also confirm the direction is within the corresponding actions dict

        elif object in interactions:
            #object specific interactions require an object so this must be checked first

            if action["type"] == "interactional actions":
                if action["code"] in interactions[object]["interactional actions"]:
                    outcome = interactions[object]["interactional actions"][action["code"]]
                
            # if it is an interactional action it only requires that the action keyword find a match inside the objects dictionary

            elif action["type"] == "directional interactional actions":
                if action["code"] in interactions[object]["directional interactional actions"]:
                    if direction:
                        if direction["code"] in interactions[object]["directional interactional actions"][action["code"]]:
                            outcome = interactions[object]["directional interactional actions"][action["code"]][direction["code"]]
                    else:
                        print(f"{action['description']} {object} in what direction?")
                        return
                # if it is directional interactional action then it will require the same conditions and more
                # it will also require the direction to find a match, within the object's action's dictionary
        else:
            print(f"It will need to be an object you've seen and can reach to {action['description']}.\n")
            return
        # this else statement activates if no object was specified but it knows you tried to interact with something.

        if isinstance(outcome, str):
            print(f"\n{outcome}\n")
            return
        elif isinstance(outcome, list):
            print(f"\n{outcome[0]}\n")
            return outcome[1]

        # this if-elif statement determines if the outcome within the dictionaries was a string or list
        # strings just get printed out, they have no actual in game effect
        # lists' first element behaves the same
        # lists' second element is used as a code to provide in game effects 

        print("You can't do that.\n")
        # if all else fails, print this to let them know the system acknowledged their input
#-------------------------------------------------------------------------------------------------
#Methods for Locations----------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------

def DarkRoom():
    # I've contained this all in a function for scalability.
    # if I were to make a second room LightRoom() then all the interactions and code can stay independent of each other
    objects = {"pocket": "unexplored"}
    # this dictionary will be assigned and unassigned objects throughout the game, to know what it is possible to interact with
    # if the object is not in the dictionary yet, then the objects name cannot be picked up by InputCommand()
    interactionDict = {
        "basic actions" : {
            "listen" : ["At first you hear nothing, but among the silence you start to make out a sound... \nBreathing, fast powerful breaths, not human... \nFootsteps, getting closer?", "sound"]
        },
        "directional actions": {
            "move" : {
                "forward": ["You bump against a hard surface. \nProbably a wall... \nYep, it's a wall.", "wall"],
                "right": ["You stumble carefully for a while.\nYou crash into a solid wooden surface, something is jutting out towards you. \nIt's a door", "closed door"],
                "left": ["You trip over something solid, \nit makes a hollow clatter and clonk as it's knocked along the ground..\nit's a bone.", "bone"],
                "backward" : "You start walking backwards but retreat...\nIf you 'listen' there's something over there."
            }
        },
        "bone" : {
            "interactional actions" : {
                "collect" : ["You pick up the bone.", "collect bone"],
                "examine" : "You struggle to see it in the dark, \nbut it's picked clean and gnawed thoroughly."
            },
            "directional interactional actions" : {
                "throw" : {
                    "forward" : ["You throw the bone as far forward as you can. \nIt makes a loud clatter as it hits the wall that echoes throughout the room. \nYou hear the padding of footsteps in the direction of the bone... \nHopefully it stays over there.", "throw forward"],
                    "left": ["You throw it back in the direction you found it.\nYou hear the padding of footsteps in the direction of the bone... \nHopefully it stays over there.", "throw left"],
                    "right": ["You throw the bone to the right.\nIt makes a loud thwump as it hits what you assume is the door.\nYou hear the padding of footsteps in the direction of the bone...\nNow it's blocking your escape...\nNice one.", "throw right"],
                    "backward" : ["You throw it behind you, in the direction you can hear a noise...\nThe sounds of breathing is replaced with violent crunches of the bone\nHopefully it stays over there.","throw backward"]
                }
            }
        },
        "dog" : {

        },
        "door" : {
            "interactional actions" : {
                "examine" : "It's hard to tell in this light but it looks like it opens towards you."
            },
            "directional interactional actions" : {
                "climb" : {
                    "upward" : "The poor design of this door does not accommodate your need for climbing.",
                    "downward" : "If only the floor wasn't in the way."
                }
            }
        },
        "pocket" : {
            "interactional actions": {
                "examine" : ["You rummage in your pockets and find an unfamiliar remote with a single button on it.", "remote found"]
            }
        },
        "remote": {
            "interactional actions": {

            }
        },
        "wall" : {
            "interactional actions" : {
                "examine" : "There's a note you have to squint to see it, it reads:\n\n 'Hi dear, if you've fallen asleep in the garage again,\n remember you've got the door remote in your pockets. Let\n the dog out while you're there too, he could use a walk.'\n\n...Huh.\nWho's this note meant for?",
                "push" : "It's not giving an inch... \nCan't fault your enthusiasm.",
                "pull" : "Really?",
            },
            "directional interactional actions" : {
                "climb" : {
                    "upward" : ["You climb the wall and bump your head on the ceiling with a mighty thud.\n'Who put that there!?' you think agrily as dust falls in your eye.\nClimb back up there and show it who's boss.","climb1"],
                    "downward" : "If only the floor wasn't in the way."
                }
            }
        },
        "metal door" : {
            "interactional actions" : {
                "examine" : "It's hard to tell in this light. \nIt doesn't look like it's going anywhere'.",
                "push" : "It shakes in place and makes a loud noise but nothing gives.",
                "pull" : "You try but there's nothing to grab."
            },
            "directional interactional actions" : {
                "climb" : {
                    "upward" : "The poor design of this door does not accommodate your need for climbing.",
                    "downward" : "If only the floor wasn't in the way."
                }
            }
        },
    }

    # This dictionary is the entire context for the room the user finds themselves in
    # it is quite quick to write new contexts and interactions but very large and hard to debug
    # if i were to do this again I would want to separate the interactions more and make use of classes to give default responses for objects.

    print("\nYou wake up surrounded by darkness.\n")
    while True:
        command = InputCommand(objects = objects)
        outcome = InterpretCommand(command, interactionDict)

    # this is the main loop that only ends by a break command when the player successfully completes the game

        if outcome == "bone":
            objects["bone"] = "not collected"
            interactionDict["bone"]["directional interactional actions"]["throw"]["forward"] = "You'll need to pick it up first."
            interactionDict["bone"]["directional interactional actions"]["throw"]["right"] = "You'll need to pick it up first."
            interactionDict["bone"]["directional interactional actions"]["throw"]["backward"] = "You'll need to pick it up first."
            interactionDict["bone"]["directional interactional actions"]["throw"]["left"] = "You'll need to pick it up first."
            interactionDict["bone"]["directional interactional actions"]["throw"]["upward"] = "You'll need to pick it up first."
            interactionDict["bone"]["directional interactional actions"]["throw"]["downward"] = "You'll need to pick it up first."
        elif outcome == "collect bone":
            objects["bone"] = "collected"
            interactionDict["directional actions"]["move"]["left"] = "The floor is slick where you found the bone. \nTread carefully."
            interactionDict["bone"]["directional interactional actions"]["throw"]["forward"] = ["You throw the bone as far forward as you can. \nIt makes a loud clatter as it hits the wall that echoes throughout the room. \nYou hear the padding of footsteps in the direction of the bone... \nHopefully it stays over there.", "throw forward"]
            interactionDict["bone"]["directional interactional actions"]["throw"]["right"] = ["You throw the bone to the right.\nIt makes a loud thwump as it hits what you assume is the door.\nYou hear the padding of footsteps in the direction of the bone...\nNow it's blocking your escape...\nNice one.", "throw right"]
            interactionDict["bone"]["directional interactional actions"]["throw"]["backward"] = ["You throw it behind you, in the direction you can hear a noise...\nThe sounds of breathing is replaced with violent crunches of the bone\nHopefully it stays over there.","throw backward"]
            interactionDict["bone"]["directional interactional actions"]["throw"]["left"] = ["You throw it back in the direction you found it.\nYou hear the padding of footsteps in the direction of the bone... \nHopefully it stays over there.", "throw left"]
            interactionDict["bone"]["directional interactional actions"]["throw"]["upward"] = ["You throw the bone with all your might straight up into the air\nYou watch with admiration of your impressive throw as it crashes back down on your face.\nIt clatters to the ground and footsteps get closer.\n It's your dog.", "bone dropped"]

            interactionDict["bone"]["directional interactional actions"]["throw"]["downward"] = ["You drop the bone on the floor.\nNot sure why you picked it up really.\nIt clatters to the ground and footsteps get closer.\n It's your dog.", "bone dropped"]

        elif outcome == "throw forward":
            objects.pop("bone")
            interactionDict["directional actions"]["move"]["backward"] = ["You walk back knowing the strange noises have gone elsewhere...\nYou can see a thin line of light at your feet just before a low metallic reverberating sound rings out. \nProbably something to do with the large metallic wall you just walked into.", "metal door"]
            interactionDict["directional actions"]["move"]["forward"] = "Let's keep away from whatevers making the noises..."
            interactionDict["basic actions"]["listen"] = "All you can hear is the chomping and breaking of bones coming from in front of you."
            if "wall" in objects:
                objects.pop("wall")
        elif outcome == "throw right":
            objects.pop("bone")
            interactionDict["directional actions"]["move"]["backward"] = ["You walk back knowing the strange noises have gone elsewhere...\nYou can see a thin line of light at your feet just before a low metallic reverberating sound rings out. \nProbably something to do with the large 'metal door' you just walked into.", "metal door"]
            interactionDict["directional actions"]["move"]["right"] = "Let's keep away from whatevers making the noises..."
            interactionDict["basic actions"]["listen"] = "All you can hear is the chomping and breaking of bones coming from your right."
            if "door" in objects:
                objects.pop("door")
        elif outcome == "throw backward":
            objects.pop("bone")
            interactionDict["directional actions"]["move"]["backward"] = "The chomping and crunching in that direction are quite discouraging."
            interactionDict["basic actions"]["listen"] = "All you can hear is the chomping and breaking of bones coming from behind you"
            if "metal door" in objects:
                objects.pop("metal door")
        elif outcome == "throw left":
            objects.pop("bone")
            interactionDict["directional actions"]["move"]["backward"] = ["You walk back knowing the strange noises have gone elsewhere...\nYou can see a thin line of light at your feet just before a low metallic reverberating sound rings out. \nProbably something to do with the large 'metal door' you just walked into.", "metal door"]
            interactionDict["directional actions"]["move"]["left"] = "Let's keep away from whatevers making the noises..."
            interactionDict["basic actions"]["listen"] = "All you can hear is the chomping and breaking of bones coming from your left"
        elif outcome == "bone dropped":
            objects.pop("bone")
            objects["dog"] = "not following"
            interactionDict["directional actions"]["move"]["backward"] = ["You walk back knowing the strange noises were just your dog...\n You can see a thin line of light at your feet just before a low metallic reverberating sound rings out. \nProbably something to do with the large metallic wall you just walked into.", "metal door"]
            interactionDict["basic actions"]["listen"] = "All you can hear is the sound of your friendly dog panting by your side"

        elif outcome == "metal door":
            objects["metal door"] = "closed"

        elif outcome == "closed door":
            objects["door"] = "closed"
            interactionDict["door"]["interactional actions"]["push"] =  "You give it a hearty thump and the door doesn't budge"
            interactionDict["door"]["interactional actions"]["pull"] = ["You use the handle and pull the door open. \nYou're free.", "opened door"]
            interactionDict["directional actions"]["move"]["right"] = "You stumble carefully for a while.\nYou crash into the door... Again."
        elif outcome == "opened door":
            objects["door"] = "open"
            interactionDict["door"]["interactional actions"]["push"] = ["You push the door closed. \nMaybe you should have been on the other side first.", "closed door"]
            interactionDict["door"]["interactional actions"]["pull"] = "it's already open."
            interactionDict["directional actions"]["move"]["right"] = ["You've escaped with your life.", "exit"]

        elif outcome == "remote found":
            objects["pocket"] = "checked"
            objects["remote"] = "not pressed"
            interactionDict["pocket"]["interactional actions"]["check"] = "There's nothing in here anymore.\n"
            interactionDict["remote"]["interactional actions"]["push"] = ["You press the button and an auditory click sounds behind you.\nLight floods the area and initially blinds you. \nAs you regain your sight you make out the shapes of trees and birds in the distance.\nA labrador comes to your side, catching you off guard as it licks your hand.\nWho's dog is this?", "remote pressed"]
            interactionDict["directional actions"]["move"]["backward"] = "It's only darkness this way."
        elif outcome == "remote pressed":
            objects["remote"] = "pressed"
            interactionDict["remote"]["interactional actions"]["push"] = ["You press the button and an auditory click sounds behind you.\nDarkness takes control once more and the feeling of stupidity sinks in.", "remote found"]
            interactionDict["directional actions"]["move"]["backward"] = ["You step gingerly into the sunlight, finally free from the dark abyss", "exit"]

        elif outcome == "sound":
            interactionDict["basic actions"]["listen"] = ["It's definitely getting closer. \nYou need to act fast.", "sound2"]
        elif outcome == "sound2":
            interactionDict["basic actions"]["listen"] = ["Oh, it's your dog. \nForgot you had that.", "found dog"]
        elif outcome == "found dog":
            objects["dog"] = "not following"
            interactionDict["directional actions"]["move"]["backward"] = ["You walk back knowing the strange noises were just your dog...\n You can see a thin line of light at your feet just before a low metallic reverberating sound rings out. \nProbably something to do with the large metallic wall you just walked into.", "metal door"]
            interactionDict["basic actions"]["listen"] = "All you can hear is the sound of your friendly dog panting by your side"

        elif outcome == "wall":
            objects["wall"] = "environment"
        elif outcome == "climb1":
            interactionDict["wall"]["directional interactional actions"]["climb"]["upward"] = ["You climb the wall... Again\nYour head collides with the ceiling... Again\nCan't fault your stubbornness\nYou hear a creak and a crack, you will be victorious!", "climb2"]
        elif outcome == "climb2":
            interactionDict["wall"]["directional interactional actions"]["climb"]["upward"] = ["You climb the wall for a third time, your head armed and ready. \nYou hear a loud crack, wood splintering around you,\nblood trickling down your face..\nSunlight.\n\nYou've made it through your garage ceiling.. Well done.", "exit"]

        if outcome == "exit":
            break
    # this list of outcomes contain all the changes to the interactionsDict, 
    # the more interactions I make the more cumbersome and hard to follow it becomes
    # if I were to do this again I would want the objects to contain their own logic and detections
    # to keep it modular.

#-------------------------------------------------------------------------------------------------
# Main Script-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
print(f"\nWelcome to your Text Adventure. \nYou're about to wake up, whereabouts unknown.\n \nYou'll no doubt feel groggy so use clear instructions to help you navigate your surroundings\n'go', go where? \n'climb ladder', climb it up or down? \n'look', look at what? \nYou get the idea... \n \nGood luck.")
currentArea = 0
areaDict = {0: DarkRoom}
# the area the player is in, and a dictionary to tell what method to use in each area
areaDict[currentArea]()