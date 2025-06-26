from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font
from PIL import Image


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/vboxuser/Schreibtisch/Tracker-Schulweg-SoftwareEngineering-Projekt/GUI/assets")


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)

class gesperrtpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.canvas = tk.Canvas(
            self,
            bg="#353333",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.create_button("entsperren.png", 1280.0, 0.0, 
                          lambda: self.handle_unlock(), 640.0, 1080.0)

        self.create_button("ausschalten.png", 51.0, 929.0,
                          lambda: print("Shutdown clicked"), 100.0, 100.0) #ausschaltenfunktion einfügen
        
        # Platzhalter für kartenfunktion - Meeting mit Hossein/Mohammed
        self.karte_image = tk.PhotoImage(file=relative_to_assets("karte.png"))
        self.canvas.create_image(640.0, 540.0, image=self.karte_image)

    def create_button(self, image_path, x, y, command, width, height):
        img = tk.PhotoImage(file=relative_to_assets(image_path))
        btn = tk.Button(
            self,
            image=img,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat"
        )
        btn.image = img  
        btn.place(x=x, y=y, width=width, height=height)
        return btn

    def handle_unlock(self):
        from start import startpage
        print("Unlock attempt")
        #einfügen des öffnen eines entry feldes
        #import pin.py -check pin if else für pin abfrage
        self.controller.show_frame(startpage)