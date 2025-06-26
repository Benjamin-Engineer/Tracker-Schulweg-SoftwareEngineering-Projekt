from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/vboxuser/Schreibtisch/Tracker-Schulweg-SoftwareEngineering-Projekt/GUI/assets")


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)
    
class einstellungenpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        from standorte_menü import standorte_menüpage
        from routen_menü import routen_menüpage
        from start import startpage
        from tracking import trackingpage
        from planer import planerpage
        from pin_ändern import pin_ändernpage
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

        self.create_button("export_grau.png", 1280, 0, 
                           lambda: print("Export clicked"), 640, 216), #exportfunktion einfügen
        self.create_button("einstellungen.png", 1280, 216, 
                           lambda: print("Already on Einstellungen"), 640, 216), #nichts ausgeben?
        self.create_button("standorte_grau.png", 1280, 432, 
                           lambda: self.controller.show_frame(standorte_menüpage), 640, 216),
        self.create_button("routen_grau.png", 1280, 648, 
                           lambda: self.controller.show_frame(routen_menüpage), 640, 216),
        self.create_button("start_grau.png", 1280, 864, 
                           lambda: self.controller.show_frame(trackingpage), 640, 216) #funktion einfügen start tracking
        self.create_button("planer.png", 738, 312, 
                         lambda: self.controller.show_frame(planerpage), 440, 240)
        self.create_button("pin_ändern.png", 102, 312, 
                         lambda: self.controller.show_frame(pin_ändernpage), 440, 240)
        self.create_button("zurück_einstellungen.png", 500, 804, 
                         lambda: self.controller.show_frame(startpage), 280, 120)

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
