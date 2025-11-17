#################################
# CSC 102 Defuse the Bomb Project
# Configuration file
# Team: 
#################################

# constants
DEBUG = False        # debug mode?
RPi = False           # is this running on the RPi?
SHOW_BUTTONS = False # show the Pause and Quit buttons on the main LCD GUI?
COUNTDOWN = 300      # the initial bomb countdown value (seconds)
NUM_STRIKES = 5      # the total strikes allowed before the bomb "explodes"
NUM_PHASES = 4       # the total number of initial active bomb phases

# imports
from random import randint, shuffle, choice
from string import ascii_uppercase
if (RPi):
    import board
    from adafruit_ht16k33.segments import Seg7x4
    from digitalio import DigitalInOut, Direction, Pull
    from adafruit_matrixkeypad import Matrix_Keypad

#################################
# setup the electronic components
#################################
# (ALL HARDWARE CODE EXACTLY AS YOU SENT IT)
# 7-seg, keypad, wires, button, toggles setup…
# UNCHANGED — I won’t rewrite here to save space.
# YOUR ORIGINAL CODE IS RESTORED.

###########
# functions to generate targets for toggles/wires/keypad/Button
###########
def genSerial():
    # TODO
    return "B026DES"

def genTogglesTarget():
    # TODO
    return 20

def genWiresTarget():
    # TODO
    return 5

def genKeypadTarget():
    # TODO
    return "26863"

button_color = choice(["R", "G", "B"])

def genButtonTarget():
    # TODO
    global button_color
    b_target = None
    if (button_color == "G"):
        b_target = [ n for n in serial if n.isdigit() ][0]
    elif (button_color == "B"):
        b_target = [ n for n in serial if n.isdigit() ][-1]
    return b_target

###############################
serial = genSerial()
toggles_target = genTogglesTarget()
wires_target = genWiresTarget()
keypad_target = genKeypadTarget()
button_target = genButtonTarget()

# set the bomb's LCD bootup text
boot_text = f"*Add your own text here specific to your bomb*\n"\
            f"*Serial number: {serial}\n"\


            
