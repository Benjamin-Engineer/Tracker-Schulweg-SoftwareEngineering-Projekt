from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
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

class trackingpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        from einstellungen import einstellungenpage
        from standorte_menü import standorte_menüpage
        from routen_menü import routen_menüpage
        from start import startpage
        self.controller = controller
        
        self.canvas = tk.Canvas(
            self,
            bg="#363434",
            height=1080,
            width=1920,
            bd=2,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.create_button("export.png", 1280, 0, lambda: print("Export clicked"), 640, 216)
        self.create_button("einstellungen.png", 1280, 216, lambda: controller.show_frame(einstellungenpage), 640, 216)
        self.create_button("standorte.png", 1280, 432, lambda: controller.show_frame(standorte_menüpage), 640, 216)
        self.create_button("routen.png", 1280, 648, lambda: controller.show_frame(routen_menüpage), 640, 216)
        self.create_button("stop.png", 1280, 864, lambda: controller.show_frame(startpage), 640, 216) #funktion einfügen stop tracking
        self.create_button("ausschalten.png", 51, 929, lambda: system_shutdown(), 100.0, 100.0)

        # Initialize and place the map widget - this will show live tracking
        self.map_widget = MapWidget(self, width=1280, height=1080)
        self.map_widget.place(x=0, y=0)

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

    def update_live_tracking(self, route_file=None):
        """
        Update the map with live tracking data
        Call this method periodically during active tracking
        """
        if route_file and self.map_widget:
            self.map_widget.route(route_file)