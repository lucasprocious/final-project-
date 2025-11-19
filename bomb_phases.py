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

class Lcd(Frame):
    # (ALL CODE UNCHANGED)
    # full original code restored…
    pass

class PhaseThread(Thread):
    # unchanged
    pass

class Timer(PhaseThread):
    # unchanged
    pass

class Keypad(PhaseThread):
    class Keypad(PhaseThread):
    def run(self):
        # Import math question from configs
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

  

class Wires(PhaseThread):
    def __init__(self, component, target, name="Wires"):
        super().__init__(name, component, target)

    def run(self):
        # TODO
        pass

    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # TODO
            pass

class Button(PhaseThread):
    # unchanged
    pass

class Toggles(PhaseThread):
    def __init__(self, component, target, name="Toggles"):
        super().__init__(name, component, target)

    def run(self):
        # TODO
        pass

    def __str__(self):
        if (self._defused):
            return "DEFUSED"
        else:
            # TODO
            pass
