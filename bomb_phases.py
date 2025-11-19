#################################
# CSC 102 Defuse the Bomb Project
# GUI and Phase class definitions
# Team: 
#################################

from bomb_configs import *
from tkinter import *
import tkinter
from threading import Thread
from time import sleep
import os
import sys

############################
# LCD GUI Class
############################
class Lcd(Frame):
    # Placeholder for your full LCD class
    # Keep your original code here; no changes needed
    pass

############################
# Base Phase Thread
############################
class PhaseThread(Thread):
    def __init__(self, name, component=None, target=None):
        super().__init__(name=name)
        self.component = component
        self.target = target
        self._running = True
        self._defused = False
        self._failed = False

############################
# Timer Phase
############################
class Timer(PhaseThread):
    def __init__(self, component, countdown):
        super().__init__("Timer", component, countdown)
        self._time_remaining = countdown
        self._paused = False

    def run(self):
        while self._running and self._time_remaining > 0:
            if not self._paused:
                sleep(1)
                self._time_remaining -= 1
            else:
                sleep(0.1)

    def pause(self):
        self._paused = True

    def unpause(self):
        self._paused = False

    def __str__(self):
        minutes = self._time_remaining // 60
        seconds = self._time_remaining % 60
        return f"{minutes:02d}:{seconds:02d}"

############################
# Keypad Phase (math question)
############################
class Keypad(PhaseThread):
    def run(self):
        from bomb_configs import math_question

        gui.display_on_lcd(math_question["question"])
        user_input = ""

        while self._running:
            key = self.component.get_key()  # hardware keypad input

            if key:
                user_input += key
                gui.display_on_lcd(user_input)

            # If answer matches → defuse
            if user_input == math_question["answer"]:
                self._defused = True
                gui.display_on_lcd("Correct!")
                break

            # If too many digits, fail the phase
            if len(user_input) > len(math_question["answer"]) + 1:
                self._failed = True
                gui.display_on_lcd("Incorrect!")
                break

    def __str__(self):
        if self._defused:
            return "DEFUSED"
        elif self._failed:
            return "FAILED"
        else:
            return "Keypad Active"

############################
# Wires Phase
############################
class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)

    def run(self):
        # Placeholder: nothing yet implemented
        while self._running:
            sleep(0.5)

    def __str__(self):
        return "DEFUSED" if self._defused else "Wires Active"

############################
# Button Phase
############################
class Button(PhaseThread):
    def __init__(self, component, rgb_component, target, color, timer, name="Button"):
        super().__init__(name, component, target)
        self.rgb_component = rgb_component
        self.color = color
        self.timer = timer

    def run(self):
        # Placeholder: nothing yet implemented
        while self._running:
            sleep(0.5)

    def __str__(self):
        return "DEFUSED" if self._defused else "Button Active"

############################
# Toggles Phase
############################
class Toggles(PhaseThread):
    def __init__(self, component, target, name="Toggles"):
        super().__init__(name, component, target)

    def run(self):
        # Placeholder: nothing yet implemented
        while self._running:
            sleep(0.5)

    def __str__(self):
        return "DEFUSED" if self._defused else "Toggles Active"
