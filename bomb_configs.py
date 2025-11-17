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

# --- NEW: globals used by multiple generators ---
serial_a = 0
serial_b = 0

#################################
# setup the electronic components
#################################
# (keep all your existing hardware setup code the same...)
# 7-seg, keypad, wires, button, toggles definitions stay as-is

###########
# functions to generate targets for toggles/wires/keypad/Button
###########

def genSerial():
    """
    Generate a math-themed serial number.
    Example: S4358SUM  where 43 and 58 are the two numbers to add.
    """
    global serial_a, serial_b

    serial_a = randint(10, 99)
    serial_b = randint(10, 99)

    # S[aa][bb]SUM  -> players can be told:
    # "Add the two middle numbers in the serial."
    return f"S{serial_a}{serial_b}SUM"


def genKeypadTarget():
    """
    Keypad = sum of the two middle numbers in the serial.
    If serial is S4358SUM, target = 43 + 58 = 101
    """
    return str(serial_a + serial_b)


def genTogglesTarget():
    """
    4 toggle switches = a 4-bit binary number (0–15).
    We use the same sum as the keypad, but clamp it to 0–15.
    """
    value = (serial_a + serial_b) % 16
    return value  # interpreted as an integer the toggles must represent


def genWiresTarget():
    """
    5 wires, indexed to the player as 1..5.
    Math rule: only PRIME-numbered wires should be cut.
    Prime indices in {1..5} = 2, 3, 5 -> zero-based: 1, 2, 4
    """
    prime_indices_1_based = [2, 3, 5]
    return [p - 1 for p in prime_indices_1_based]  # store zero-based


# generate the color of the pushbutton (which determines how to defuse the phase)
button_color = choice(["R", "G", "B"])

def genButtonTarget():
    """
    Make the button mathy:
    - R (red)  = press & release anytime (no math)
    - G (green)= release when timer seconds are a multiple of 3
    - B (blue) = release when timer seconds are a multiple of 5
    We’ll store the divisor as an int; R will store None.
    """
    global button_color

    if button_color == "R":
        return None          # any release is fine
    elif button_color == "G":
        return 3             # multiple of 3
    else:  # "B"
        return 5             # multiple of 5


###############################
# These lines stay at the bottom of configs
serial = genSerial()
toggles_target = genTogglesTarget()
wires_target = genWiresTarget()
keypad_target = genKeypadTarget()
button_target = genButtonTarget()

# set the bomb's LCD bootup text (math-themed instructions)
boot_text = (
    "MATH CORE MELTDOWN v1.0\n"
    f"Serial number: {serial}\n"
    "KEYPAD: Enter the sum of the two middle numbers in the serial.\n"
    "WIRES: Cut only the PRIME-numbered wires (2, 3, 5,...).\n"
    "TOGGLES: Set switches so their binary value matches the keypad answer (mod 16).\n"
    "BUTTON: Follow the color rule -\n"
    "   RED: release anytime.\n"
    "   GREEN: release when seconds are a multiple of 3.\n"
    "   BLUE: release when seconds are a multiple of 5.\n"
)

            
