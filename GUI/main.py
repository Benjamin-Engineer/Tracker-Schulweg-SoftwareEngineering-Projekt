from pathlib import Path
import tkinter as tk
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font

from mainapp import mainappclass

running = True 

while running == True:
    app = mainappclass()
    app.mainloop()