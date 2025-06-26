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


class standortepage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        from standorte_menü import standorte_menüpage
        from start import startpage
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

        # platzhalter karte - Meeting mit Hossein/Mohammed
        self.karte_image = tk.PhotoImage(file=relative_to_assets("karte.png"))
        self.canvas.create_image(640.0, 540.0, image=self.karte_image)

        self.create_button("ausschalten.png", 51.0, 929.0, 
                         lambda: print("Shutdown clicked"), 100.0, 100.0) #funktion ausschalten einfügen

        self.canvas.create_rectangle(
            1278.0, 0.0, 1919.0, 1079.0,
            fill="#353333", outline="#FFFFFF"
        )

        self.create_button("standorte.png", 1280.0, 0.0,
                         lambda: print("Standorte clicked"), 640.0, 216.0) #nichts tun

        self.create_button("ausklappen.png", 1071.0, 0.0,
                         lambda: self.controller.show_frame(standorte_menüpage), 
                         218.0, 218.0)

        # plathalter dateiaufruf json
        self.canvas.create_rectangle(
            1282.0, 218.0, 1918.0, 918.0,
            fill="#000000", outline=""
        )

        self.create_button("zurück.png", 1460.0, 930.0,
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
