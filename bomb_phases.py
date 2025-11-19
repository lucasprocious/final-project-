#################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: 
#################################

# import the configs
from bomb_configs import *
# other imports
from tkinter import *
import tkinter
from threading import Thread
from time import sleep
import os
import sys

#########
# classes
#########
# the LCD display GUI
class Lcd(Frame):
    def __init__(self, window):
        super().__init__(window, bg="black")
        # make the GUI fullscreen
        window.attributes("-fullscreen", True)
        # we need to know about the timer (7-segment display) to be able to pause/unpause it
        self._timer = None
        # we need to know about the pushbutton to turn off its LED when the program exits
        self._button = None
        # setup the initial "boot" GUI
        self.setupBoot()

    # sets up the LCD "boot" GUI
    def setupBoot(self):
        # set column weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)
        # the scrolling informative "boot" text
        self._lscroll = Label(self, bg="black", fg="white", font=("Courier New", 14), text="", justify=LEFT)
        self._lscroll.grid(row=0, column=0, columnspan=3, sticky=W)
        self.pack(fill=BOTH, expand=True)

    # sets up the LCD GUI
    def setup(self):
        # the timer
        self._ltimer = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Time left: ")
        self._ltimer.grid(row=1, column=0, columnspan=3, sticky=W)
        # the math challenge status
        self._lmath = Label(self, bg="black", fg="#ffff00", font=("Courier New", 18), text="Math Challenge: ", justify=LEFT)
        self._lmath.grid(row=2, column=0, columnspan=3, sticky=W)
        # the keypad passphrase
        self._lkeypad = Label(self, bg="black", fg="#666666", font=("Courier New", 18), text="Keypad phase: LOCKED")
        self._lkeypad.grid(row=3, column=0, columnspan=3, sticky=W)
        # the jumper wires status
        self._lwires = Label(self, bg="black", fg="#666666", font=("Courier New", 18), text="Wires phase: LOCKED")
        self._lwires.grid(row=4, column=0, columnspan=3, sticky=W)
        # the pushbutton status
        self._lbutton = Label(self, bg="black", fg="#666666", font=("Courier New", 18), text="Button phase: LOCKED")
        self._lbutton.grid(row=5, column=0, columnspan=3, sticky=W)
        # the toggle switches status
        self._ltoggles = Label(self, bg="black", fg="#666666", font=("Courier New", 18), text="Toggles phase: LOCKED")
        self._ltoggles.grid(row=6, column=0, columnspan=2, sticky=W)
        # the strikes left
        self._lstrikes = Label(self, bg="black", fg="#00ff00", font=("Courier New", 18), text="Strikes left: ")
        self._lstrikes.grid(row=6, column=2, sticky=W)
        if (SHOW_BUTTONS):
            # the pause button (pauses the timer)
            self._bpause = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Pause", anchor=CENTER, command=self.pause)
            self._bpause.grid(row=7, column=0, pady=40)
            # the quit button
            self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
            self._bquit.grid(row=7, column=2, pady=40)

    # unlock other phases on the GUI
    def unlockPhases(self):
        self._lkeypad["fg"] = "#00ff00"
        self._lkeypad["text"] = "Keypad phase: "
        self._lwires["fg"] = "#00ff00"
        self._lwires["text"] = "Wires phase: "
        self._lbutton["fg"] = "#00ff00"
        self._lbutton["text"] = "Button phase: "
        self._ltoggles["fg"] = "#00ff00"
        self._ltoggles["text"] = "Toggles phase: "

    # lets us pause/unpause the timer (7-segment display)
    def setTimer(self, timer):
        self._timer = timer

    # lets us turn off the pushbutton's RGB LED
    def setButton(self, button):
        self._button = button

    # pauses the timer
    def pause(self):
        if (RPi):
            self._timer.pause()

    # setup the conclusion GUI (explosion/defusion)
    def conclusion(self, success=False):
        # destroy/clear widgets that are no longer needed
        self._lscroll["text"] = ""
        self._ltimer.destroy()
        self._lmath.destroy()
        self._lkeypad.destroy()
        self._lwires.destroy()
        self._lbutton.destroy()
        self._ltoggles.destroy()
        self._lstrikes.destroy()
        if (SHOW_BUTTONS):
            self._bpause.destroy()
            self._bquit.destroy()

        # reconfigure the GUI
        # the retry button
        self._bretry = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Retry", anchor=CENTER, command=self.retry)
        self._bretry.grid(row=1, column=0, pady=40)
        # the quit button
        self._bquit = tkinter.Button(self, bg="red", fg="white", font=("Courier New", 18), text="Quit", anchor=CENTER, command=self.quit)
        self._bquit.grid(row=1, column=2, pady=40)

    # re-attempts the bomb (after an explosion or a successful defusion)
    def retry(self):
        # re-launch the program (and exit this one)
        os.execv(sys.executable, ["python3"] + [sys.argv[0]])
        exit(0)

    # quits the GUI, resetting some components
    def quit(self):
        if (RPi):
            # turn off the 7-segment display
            self._timer._running = False
            self._timer._component.blink_rate = 0
            self._timer._component.fill(0)
            # turn off the pushbutton's LED
            for pin in self._button._rgb:
                pin.value = True
        # exit the application
        exit(0)

# template (superclass) for various bomb components/phases
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name, daemon=True)
        # phases have an electronic component (which usually represents the GPIO pins)
        self._component = component
        # phases have a target value (e.g., a specific combination on the keypad, the proper jumper wires to "cut", etc)
        self._target = target
        # phases can be successfully defused
        self._defused = False
        # phases can be failed (which result in a strike)
        self._failed = False
        # phases have a value (e.g., a pushbutton can be True/Pressed or False/Released, several jumper wires can be "cut"/False, etc)
        self._value = None
        # phase threads are either running or not
        self._running = False

# the timer phase
class Timer(PhaseThread):
    def __init__(self, component, initial_value, name="Timer"):
        super().__init__(name, component)
        # the default value is the specified initial value
        self._value = initial_value
        # is the timer paused?
        self._paused = False
        # initialize the timer's minutes/seconds representation
        self._min = ""
        self._sec = ""
        # by default, each tick is 1 second
        self._interval = 1

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            if (not self._paused):
                # update the timer and display its value on the 7-segment display
                self._update()
                self._component.print(str(self))
                # wait 1s (default) and continue
                sleep(self._interval)
                # the timer has expired -> phase failed (explode)
                if (self._value == 0):
                    self._running = False
                self._value -= 1
            else:
                sleep(0.1)

    # updates the timer (only internally called)
    def _update(self):
        self._min = f"{self._value // 60}".zfill(2)
        self._sec = f"{self._value % 60}".zfill(2)

    # pauses and unpauses the timer
    def pause(self):
        # toggle the paused state
        self._paused = not self._paused
        # blink the 7-segment display when paused
        self._component.blink_rate = (2 if self._paused else 0)

    # returns the timer as a string (mm:ss)
    def __str__(self):
        return f"{self._min}:{self._sec}"

# the math challenge phase (must be completed before other phases unlock)
class MathChallenge(PhaseThread):
    def __init__(self, component, questions, name="MathChallenge"):
        super().__init__(name, component)
        # the math questions to solve
        self._questions = questions
        # current question index
        self._current_question = 0
        # the current answer being entered
        self._value = ""
        # track if all questions are answered
        self._all_complete = False

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # process keys when keypad key(s) are pressed
            if (self._component.pressed_keys):
                # debounce
                while (self._component.pressed_keys):
                    try:
                        # just grab the first key pressed if more than one were pressed
                        key = self._component.pressed_keys[0]
                    except:
                        key = ""
                    sleep(0.1)
                
                # handle special keys
                if (key == "*"):
                    # clear the current input
                    self._value = ""
                elif (key == "#"):
                    # submit the answer
                    if (self._value):
                        correct_answer = self._questions[self._current_question]['answer']
                        if (self._value == correct_answer):
                            # correct answer!
                            self._current_question += 1
                            self._value = ""
                            # check if all questions are answered
                            if (self._current_question >= len(self._questions)):
                                self._defused = True
                                self._all_complete = True
                                self._running = False
                        else:
                            # wrong answer -> strike
                            self._failed = True
                            self._value = ""
                else:
                    # add the digit to the current answer
                    self._value += str(key)
            
            sleep(0.1)

    # returns the current question and answer progress as a string
    def __str__(self):
        if (self._all_complete):
            return "ALL QUESTIONS SOLVED - PHASES UNLOCKED!"
        else:
            question_text = self._questions[self._current_question]['question']
            return f"Q{self._current_question + 1}/{len(self._questions)}: {question_text} = {self._value}_"

# the keypad phase (now only active after math challenge)
class Keypad(PhaseThread):
    def __init__(self, component, target, name="Keypad"):
        super().__init__(name, component, target)
        # the default value is an empty string
        self._value = ""
        # is this phase locked?
        self._locked = True

    # unlocks the phase
    def unlock(self):
        self._locked = False

    # runs the thread
    def run(self):
        self._running = True
        while (self._running):
            # only process if unlocked
            if (not self._locked):
                # process keys when keypad key(s) are pressed
                if (self._component.pressed_keys):
                    # debounce
                    while (self._component.pressed_keys):
                        try:
                            # just grab the first key pressed if more than one were pressed
                            key = self._component.pressed_keys[0]
                        except:
                            key = ""
                        sleep(0.1)
                    # log the key
                    self._value += str(key)
                    # the combination is correct -> phase defused
                    if (self._value == self._target):
                        self._defused = True
                    # the combination is incorrect -> phase failed (strike)
                    elif (self._value != self._target[0:len(self._value)]):
                        self._failed = True
            sleep(0.1)

    # returns the keypad combination as a string
    def __str__(self):
        if (self._locked):
            return "LOCKED"
        elif (self._defused):
            return "DEFUSED"
        else:
            return self._value

# the jumper wires phase
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)
        self._locked = True

    def unlock(self):
        self._locked = False

    # runs the thread
    def run(self):
        # TODO
        pass

    # returns the jumper wires state as a string
    def __str__(self):
        if (self._locked):
            return "LOCKED"
        elif (self._defused):
            return "DEFUSED"
        else:
            # TODO
            return "TODO"

# the pushbutton phase
class Button(PhaseThread):
    def __init__(self, component_state, component_rgb, target, color, timer, name="Button"):
        super().__init__(name, component_state, target)
        # the default value is False/Released
        self._value = False
        # has the pushbutton been pressed?
        self._pressed = False
        # we need the pushbutton's RGB pins to set its color
        self._rgb = component_rgb
        # the pushbutton's randomly selected LED color
        self._color = color
        # we need to know about the timer (7-segment display) to be able to determine correct pushbutton releases in some cases
        self._timer = timer
        self._locked = True

    def unlock(self):
        self._locked = False

    # runs the thread
    def run(self):
        self._running = True
        # set the RGB LED color
        self._rgb[0].value = False if self._color == "R" else True
        self._rgb[1].value = False if self._color == "G" else True
        self._rgb[2].value = False if self._color == "B" else True
        while (self._running):
            if (not self._locked):
                # get the pushbutton's state
                self._value = self._component.value
                # it is pressed
                if (self._value):
                    # note it
                    self._pressed = True
                # it is released
                else:
                    # was it previously pressed?
                    if (self._pressed):
                        # check the release parameters
                        # for R, nothing else is needed
                        # for G or B, a specific digit must be in the timer (sec) when released
                        if (not self._target or self._target in self._timer._sec):
                            self._defused = True
                        else:
                            self._failed = True
                        # note that the pushbutton was released
                        self._pressed = False
            sleep(0.1)

    # returns the pushbutton's state as a string
    def __str__(self):
        if (self._locked):
            return "LOCKED"
        elif (self._defused):
            return "DEFUSED"
        else:
            return str("Pressed" if self._value else "Released")

# the toggle switches phase
class Toggles(PhaseThread):
    def __init__(self, component, target, name="Toggles"):
        super().__init__(name, component, target)
        self._locked = True

    def unlock(self):
        self._locked = False

    # runs the thread
    def run(self):
        # TODO
        pass

    # returns the toggle switches state as a string
    def __str__(self):
        if (self._locked):
            return "LOCKED"
        elif (self._defused):
            return "DEFUSED"
        else:
            # TODO
            return "TODO"
