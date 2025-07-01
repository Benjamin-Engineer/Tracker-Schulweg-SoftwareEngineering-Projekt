from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font
from PIL import Image

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from start_stop import toggle_status
from shutdown import system_shutdown

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/GUI/assets")


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)


class standorte_menüpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        from einstellungen import einstellungenpage
        from standorte import standortepage
        from routen_menü import routen_menüpage
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

        self.create_button("export_grau.png", 1280, 0, 
                           lambda: print("Export clicked"), 640, 216) #einfügen exportfunktion
        self.create_button("einstellungen_grau.png", 1280, 216, 
                           lambda: self.controller.show_frame(einstellungenpage), 640, 216)
        self.create_button("standorte.png", 1280, 432, 
                           lambda: print("standorte clicked"), 640, 216)
        self.create_button("routen_grau.png", 1280, 648, 
                           lambda: self.controller.show_frame(routen_menüpage), 640, 216)
        self.create_button("start_grau.png", 1280, 864, 
                           lambda: toggle_status(), 640, 216) #funktion einfügen start tracking
        
        # platzhalter karte - Meeting mit Hossein/Mohammed
        self.karte_image = tk.PhotoImage(file=relative_to_assets("karte.png"))
        self.canvas.create_image(640.0, 540.0, image=self.karte_image)

        text_img = tk.PhotoImage(file=relative_to_assets("standorte.png"))
        self.canvas.create_image(960.0, 110.0, image=text_img)
        self.canvas.image = text_img  

        self.canvas.create_line(
            640.0, 0.0, 640.0, 1080.0, fill="#FFFFFF", width=4
        )
        self.canvas.create_rectangle( #platzhalter dateiaufruf json
            642.0, 218.0, 1277.0, 918.0, fill="#000000"
        )
        self.canvas.create_rectangle(
            2.0, 2.0, 638.0, 1078.0, fill="#363434"
        )

        self.create_button("ausschalten.png", 51.0, 929.0,
                          lambda: system_shutdown(), 100.0, 100.0) #ausschaltenfunktion einfügen
        
        self.create_button("zurück.png", 819.0, 930.0,
                          lambda: self.controller.show_frame(startpage), 280.0, 97.0)

        self.create_button("einklappen.png", 425.0, 0.0,
                          lambda: self.controller.show_frame(standortepage), 215.0, 216.0)
        
        self.canvas.create_rectangle(638.0, 216.0, 642.0, 1080.0, fill="#FFFFFF", outline="")

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
