from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/Danny/Desktop/software-projekt_schulwegtracker/SCRUM21/Tracker-Schulweg-SoftwareEngineering-Projekt/GUI/assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class startpage(tk.Frame):
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

        self.create_button("export.png", 1280, 0, lambda: print("Export clicked"))
        self.create_button("einstellungen.png", 1280, 216, lambda: controller.show_frame(einstellungenpage))
        self.create_button("standorte.png", 1280, 432, lambda: controller.show_frame(standorte_menüpage))
        self.create_button("routen.png", 1280, 648, lambda: controller.show_frame(routen_menüpage))
        self.create_button("start.png", 1280, 864, lambda: controller.show_frame(trackingpage)) #funktion einfügen start tracking
        self.create_button("ausschalten.png", 51, 929, lambda: print("Shutdown"))

        # Platzhalter für Kartenfunktion - Meeting mit Hossein
        self.karte_image = tk.PhotoImage(file=relative_to_assets("karte.png"))
        self.canvas.create_image(640.0, 540.0, image=self.karte_image)

    def create_button(self, image_path, x, y, command):
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
        btn.place(x=x, y=y, width=640, height=216)