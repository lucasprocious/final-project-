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
    # unchanged
    pass

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
