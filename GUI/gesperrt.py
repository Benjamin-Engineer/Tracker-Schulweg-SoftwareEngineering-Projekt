from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font
from PIL import Image

import sys
import os

from pin import check_pin

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shutdown import system_shutdown

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/GUI/assets")


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)

class gesperrtpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.font = ("Inter", 36)

        self.canvas = tk.Canvas(
            self,
            bg="#363434",
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
                          lambda: system_shutdown(), 100.0, 100.0) #ausschaltenfunktion einfügen
        
        
        self.canvas.create_rectangle(1425.0, 200.0, 1775.0, 363.0, fill="#FFFFFF", outline="#FFFFFF")
        self.eingabe_pin = self.create_entry(1427.0, 202.0)
    
        
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
            relief="flat",
            background="#363434"
        )
        btn.image = img  
        btn.place(x=x, y=y, width=width, height=height)
        return btn
    
    def create_entry(self, x, y):
        entry = tk.Entry(
            self,
            bd=2,
            bg="#363434",
            fg="#FFFFFF",
            highlightthickness=0,
            justify="center",
            font=self.font
        )
        entry.place(x=x, y=y, width=343.0, height=155.0)
        return entry

    def handle_unlock(self):
        from start import startpage
        if(check_pin(self.eingabe_pin.get().strip())):{
        self.controller.show_frame(startpage)
        }
        else :{
            print("Falsche PIN! Bitte erneut eingeben.")
        }
