from pathlib import Path
import tkinter as tk
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font

from mainapp import mainappclass

OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"GUI\assets") # WINDOWS
#ASSETS_PATH = OUTPUT_PATH / Path(r"GUI/assets") # LINUX / MAC
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/vboxuser/Schreibtisch/Tracker-Schulweg-SoftwareEngineering-Projekt/GUI/assets") # VIRTUALBOX (Fall GUI/assets nicht klappt)


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)

if __name__ == "__main__":
    app = mainappclass()
    app.mainloop()