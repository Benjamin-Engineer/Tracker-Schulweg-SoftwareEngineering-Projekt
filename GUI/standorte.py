from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font
from PIL import Image

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shutdown import system_shutdown
from map_widget import MapWidget

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/GUI/assets")


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
            bg="#363434",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Initialize and place the map widget for location viewing
        self.map_widget = MapWidget(self, width=1280, height=1080)
        self.map_widget.place(x=0, y=0)

        self.create_button("ausschalten.png", 51.0, 929.0, 
                        lambda: system_shutdown(), 100.0, 100.0) #funktion ausschalten einfügen

        self.canvas.create_rectangle(
            1278.0, 0.0, 1919.0, 1079.0,
            fill="#363434", outline="#FFFFFF"
        )

        self.create_button("standorte.png", 1280.0, 0.0,
                         lambda: print("Standorte clicked"), 640.0, 216.0) #nichts tun

        self.create_button("ausklappen.png", 1071.0, 0.0,
                         lambda: self.controller.show_frame(standorte_menüpage), 
                         208.0, 217.0)
        self.canvas.create_rectangle(1278.0, -2.0, 1282.0, 1080.0, fill="#FFFFFF", outline="")

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
            relief="flat",
            background="#363434"
        )
        btn.image = img  
        btn.place(x=x, y=y, width=width, height=height)
        return btn

    def display_location(self, location_file):
        """
        Display a specific location on the map
        """
        if location_file and self.map_widget:
            self.map_widget.standort(location_file)
