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
    # configure the remaining GUI widgets
    gui.setup()
    # setup the phase threads, execute them, and check their statuses
    if (RPi):
        setup_phases()
        check_phases()
   
# sets up the phase threads
def setup_phases():
    global timer, math_challenge, keypad, wires, button, toggles
    
    # setup the timer thread
    timer = Timer(component_7seg, COUNTDOWN)
    # bind the 7-segment display to the LCD GUI so that it can be paused/unpaused from the GUI
    gui.setTimer(timer)
    
    # setup the math challenge thread (must be completed first!)
    math_challenge = MathChallenge(component_keypad, math_questions)
    
    # setup the other phase threads (initially locked)
    keypad = Keypad(component_keypad, keypad_target)
    wires = Wires(component_wires, wires_target)
    button = Button(component_button_state, component_button_RGB, button_target, button_color, timer)
    toggles = Toggles(component_toggles, toggles_target)
    
    # bind the pushbutton to the LCD GUI so that its LED can be turned off when we quit
    gui.setButton(button)

    # start the phase threads
    timer.start()
    math_challenge.start()
    keypad.start()
    wires.start()
    button.start()
    toggles.start()

# checks the phase threads
def check_phases():
    global active_phases, math_unlocked
    
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
    
    # check the math challenge first
    if (math_challenge._running):
        # update the GUI
        gui._lmath["text"] = f"Math Challenge: {math_challenge}"
        # the phase has failed -> strike
        if (math_challenge._failed):
            strike()
            # reset the math challenge
            math_challenge._failed = False
    # math challenge is complete -> unlock other phases
    elif (not math_unlocked and math_challenge._defused):
        math_unlocked = True
        gui._lmath["text"] = "Math Challenge: COMPLETE!"
        gui._lmath["fg"] = "#00ff00"
        # unlock all other phases
        keypad.unlock()
        wires.unlock()
        button.unlock()
        toggles.unlock()
        # update GUI to show phases are unlocked
        gui.unlockPhases()
    
    # only check other phases if math challenge is complete
    if (math_unlocked):
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
                # reset the keypad
                keypad._failed = False
                keypad._value = ""
        # check the wires
        if (wires._running):
            # update the GUI
            gui._lwires["text"] = f"Wires: {wires}"
            # the phase is defused -> stop the thread
            if (wires._defused):
                wires._running = False
                active_phases -= 1
            # the phase has failed -> strike
            elif (wires._failed):
                strike()
                # reset the wires
                wires._failed = False
        # check the button
        if (button._running):
            # update the GUI
            gui._lbutton["text"] = f"Button: {button}"
            # the phase is defused -> stop the thread
            if (button._defused):
                button._running = False
                active_phases -= 1
            # the phase has failed -> strike
            elif (button._failed):
                strike()
                # reset the button
                button._failed = False
        # check the toggles
        if (toggles._running):
            # update the GUI
            gui._ltoggles["text"] = f"Toggles: {toggles}"
            # the phase is defused -> stop the thread
            if (toggles._defused):
                toggles._running = False
                active_phases -= 1
            # the phase has failed -> strike
            elif (toggles._failed):
                strike()
                # reset the toggles
                toggles._failed = False

    # note the strikes on the GUI
    gui._lstrikes["text"] = f"Strikes left: {strikes_left}"
    # too many strikes -> explode!
    if (strikes_left == 0):
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(1000, gui.conclusion, False)
        # stop checking phases
        return

    # the bomb has been successfully defused!
    if (active_phases == 0 and math_unlocked):
        # turn off the bomb and render the conclusion GUI
        turn_off()
        gui.after(100, gui.conclusion, True)
        # stop checking phases
        return

    # check the phases again after a slight delay
    gui.after(100, check_phases)

# handles a strike
def strike():
    global strikes_left
    
    # note the strike
    strikes_left -= 1

# turns off the bomb
def turn_off():
    # stop all threads
    timer._running = False
    math_challenge._running = False
    keypad._running = False
    wires._running = False
    button._running = False
    toggles._running = False

    # turn off the 7-segment display
    component_7seg.blink_rate = 0
    component_7seg.fill(0)
    # turn off the pushbutton's LED
    for pin in button._rgb:
        pin.value = True

######
# MAIN
######

# initialize the LCD GUI
window = Tk()
gui = Lcd(window)

# initialize the bomb strikes and active phases (i.e., not yet defused)
strikes_left = NUM_STRIKES
active_phases = NUM_PHASES
math_unlocked = False  # track if math challenge is complete

# "boot" the bomb
gui.after(100, bootup)

# display the LCD GUI
window.mainloop()
