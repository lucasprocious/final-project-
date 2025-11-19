#################################
# CSC 102 Defuse the Bomb Project
# Main program
# Team: 
#################################

# Import configs and phases
from bomb_configs import *
from bomb_phases import *
from tkinter import *
import threading
from time import sleep

############################
# Functions
############################

# Function to display text on the LCD
def display_on_lcd(message):
    if hasattr(gui, "_lscroll"):
        gui._lscroll["text"] = message

# Bootup sequence
def bootup():
    display_on_lcd(boot_text.replace("\x00", ""))

# Function to handle the bomb sequence
def start_bomb_sequence():
    # Display the math question on the LCD
    display_on_lcd(f"Solve this on the keypad:\n{math_question['question']}")

    # Wait until Keypad phase is defused
    while True:
        user_input = get_keypad_input()  # Replace with your method to read keypad input
        if user_input.strip() == math_question["answer"]:
            display_on_lcd("Correct! You may begin defusing the bomb.")
            break
        else:
            display_on_lcd("Incorrect! Try again.")

    # Setup GUI
    gui.setup()

    # Setup and start the phases
    if RPi:
        setup_phases()
        check_phases()

############################
# Helper: get keypad input
############################
def get_keypad_input():
    # This is a placeholder; replace with your hardware input method
    if RPi:
        return component_keypad.get_key()
    else:
        # Simulation mode: ask user in terminal
        return input("Enter Keypad answer: ")

############################
# Phase setup
############################
def setup_phases():
    global timer, keypad, wires, button, toggles

    # Timer
    timer = Timer(component_7seg, COUNTDOWN)
    gui.setTimer(timer)

    # Keypad
    keypad = Keypad(component_keypad, keypad_target)

    # Wires
    wires = Wires(component_wires, wires_target)

    # Button
    button = Button(component_button_state, component_button_RGB, button_target, button_color, timer)
    gui.setButton(button)

    # Toggles
    toggles = Toggles(component_toggles, toggles_target)

    # Start threads
    timer.start()
    keypad.start()
    wires.start()
    button.start()
    toggles.start()

############################
# Phase checking loop
############################
def check_phases():
    global active_phases
    active_phases = NUM_PHASES

    while active_phases > 0:
        sleep(0.5)

        # Timer check
        if not timer._running or timer._time_remaining <= 0:
            turn_off()
            gui.after(100, gui.conclusion, False)
            break
        else:
            gui._ltimer["text"] = f"Time left: {timer}"

        # Keypad check
        if keypad._running:
            gui._lkeypad["text"] = f"Combination: {keypad}"
            if keypad._defused:
                keypad._running = False
                active_phases -= 1
            elif keypad._failed:
                strike()

        # Wires check
        if wires._running:
            gui._lwires["text"] = str(wires)
            if wires._defused:
                wires._running = False
                active_phases -= 1

        # Button check
        if button._running:
            gui._lbutton["text"] = str(button)
            if button._defused:
                button._running = False
                active_phases -= 1

        # Toggles check
        if toggles._running:
            gui._ltoggles["text"] = str(toggles)
            if toggles._defused:
                toggles._running = False
                active_phases -= 1

############################
# Placeholder functions
############################
def turn_off():
    # Turn off hardware or GUI
    display_on_lcd("Bomb off!")
    timer._running = False
    keypad._running = False
    wires._running = False
    button._running = False
    toggles._running = False

def strike():
    display_on_lcd("Strike!")
    sleep(1)

############################
# Main program
############################
if __name__ == "__main__":
    # Create GUI instance
    gui = Lcd()

    # Bootup display
    bootup()

    # Start the bomb sequence (math question)
    start_bomb_sequence()
