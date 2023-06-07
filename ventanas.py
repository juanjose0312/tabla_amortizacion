from tkinter import *

class Window:

    def __init__(self, window, title, geometry):
        self.wind = window
        self.wind.title(title)
        self.wind.geometry(geometry)