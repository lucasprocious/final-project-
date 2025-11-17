#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: 
#################################

# import the configs
from bomb_configs import *
# import the phases
from bomb_phases import *

###########
# functions
###########
# generates the bootup sequence on the LCD
def bootup(n=0):
    gui._lscroll["text"] = boot_text.replace("\x00", "")
from bomb_configs import trivia_question  # Import if you use the trivia in configs

def start_bomb_sequence():
    display_on_lcd(f"Trivia: {trivia_question}")
    # Wait for user to enter the keypad answer
    while True:
        user_input = get_keypad_input()  # Replace with your method for capturing keypad input
        if user_input.strip() == "60":
            display_on_lcd("Correct! You may begin defusing the bomb.")
            proceed_to_bomb_phases()  # Your main bomb game logic
            break
        else:
            display_on_lcd("Incorrect! Please try again.")    
    # configure the remaining GUI widgets
    gui.setup()
    # setup the phase threads, execute them, and check their statuses
    if (RPi):
        setup_phases()
        check_phases()
    # if we're animating
   
# sets up the phase threads
def setup_phases():
    global timer, keypad, wires, button, toggles
    
    # setup the timer thread
    timer = Timer(component_7seg, COUNTDOWN)
    # bind the 7-segment display to the LCD GUI so that it can be paused/unpaused from the GUI
    gui.setTimer(timer)
    # setup the keypad thread
    keypad = Keypad(component_keypad, keypad_target)
    # setup the jumper wires thread
    wires = Wires(component_wires, wires_target)
    # setup the pushbutton thread
    button = Button(component_button_state, component_button_RGB, button_target, button_color, timer)
    # bind the pushbutton to the LCD GUI so that its LED can be turned off when we quit
    gui.setButton(button)
    # setup the toggle switches thread
    toggles = Toggles(component_toggles, toggles_target)

    # start the phase threads
    timer.start()
    keypad.start()
    wires.start()
    button.start()
    toggles.start()

# checks the phase threads
def check_phases():
    global active_phases
    
    # check the timer
    if (timer._running):
        # update the GUI
        gui._ltimer["text"] = f"Time left: {timer}"
    else:
        # the countdown has expired -> explode!
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, False)
        # don't check any more phases
        return
    # check the keypad
    if (keypad._running):
        # update the GUI
        gui._lkeypad["text"] = f"Combination: {keypad}"
        # the phase is defused -> stop the thread
        if (keypad._defused):
            keypad._running = False
            active_phases -= 1
        # the phase has failed -> strike
        elif (keypad._failed):
            strike()

