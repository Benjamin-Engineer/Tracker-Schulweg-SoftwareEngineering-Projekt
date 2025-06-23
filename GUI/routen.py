from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font
from PIL import Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/Danny/Desktop/software-projekt_schulwegtracker/SCRUM21/Tracker-Schulweg-SoftwareEngineering-Projekt/GUI/assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class routenpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.canvas = tk.Canvas(
            self,
            bg="#353333",
            height=1080,
            width=1920,
            bd=2,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Map image
        self.karte_image = tk.PhotoImage(file=relative_to_assets("karte.png"))
        self.canvas.create_image(640.0, 540.0, image=self.karte_image)

        self.create_button("routen.png", 1280.0, 0.0, 
                          lambda: print("Routen clicked"), 640.0, 216.0)

        self.create_button("ausschalten.png", 51.0, 929.0,
                          lambda: print("Shutdown clicked"), 100.0, 100.0) #funktion ausschalten einfügen

        self.canvas.create_rectangle(
            1278.0, 0.0, 1919.0, 1079.0,
            fill="#353333", outline="#FFFFFF"
        )

        self.create_button("ausklappen.png", 1071.0, 0.0,
                          lambda: self.controller.show_frame(routen_menüpage),
                          218.0, 218.0)

        # platzhalter dateiaufruf json
        self.canvas.create_rectangle(
            1282.0, 218.0, 1918.0, 773.0,
            fill="#000000", outline=""
        )

        self.create_button("routen_löschen.png", 1459.0, 782.0,
                          lambda: print("Delete routes clicked"), #einfügen funktion routen löschen
                          280.0, 97.67442321777344)

        self.create_button("zurück.png", 1459.0, 930.0,
                          lambda: self.controller.show_frame(startpage),
                          280.0, 97.67442321777344)

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