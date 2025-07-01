from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font
from PIL import Image

import sys
import os

import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from planner import save_entries
from start_stop import toggle_status

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/GUI/assets")


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)


class planerpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        from einstellungen import einstellungenpage
        from standorte_menü import standorte_menüpage
        from routen_menü import routen_menüpage
        from start import startpage
        self.controller = controller
        self.font = ("Inter", 36)
        
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
        
        self.create_button("export_grau.png", 1280, 0, 
                           lambda: print("Export clicked"), 640, 216)
        self.create_button("einstellungen.png", 1280, 216, 
                           lambda: self.controller.show_frame(einstellungenpage), 640, 216)
        self.create_button("standorte_grau.png", 1280, 432, 
                           lambda: self.controller.show_frame(standorte_menüpage), 640, 216)
        self.create_button("routen_grau.png", 1280, 648, 
                           lambda: self.controller.show_frame(routen_menüpage), 640, 216)
        self.create_button("start_grau.png", 1280, 864, 
                           lambda: toggle_status(), 640, 216) #funktion einfügen start tracking

        self.create_button("zurück_einstellungen.png", 500, 804,
                         lambda: self.controller.show_frame(einstellungenpage), 280, 120)
        
        self.canvas.create_rectangle(-1.0, 213.0, 1280.0, 215.0, fill="#363434", outline="")

        self.canvas.create_rectangle(0.0, 214.0, 1280.0, 218.0, fill="#FFFFFF", outline="")
        

        self.canvas.create_rectangle(100.0, 285.0, 500.0, 735.0, fill="#363434", outline="#FFFFFF")
        
        self.eingabe_von = self.create_entry(302.0, 586.0, 190.0, 137.0)
        self.eingabe_bis = self.create_entry(302.0, 437.0, 196.0, 145.0)
        
        self.create_button("hinzufügen.png", 109, 294,
                         lambda: save_entries(self.eingabe_bis.get().strip(), self.eingabe_von.get().strip()), 382, 141) # Speichern der einträge
        
        self.canvas.create_line(300.0, 436.0, 300.0, 735.0, fill="#FFFFFF")
        self.canvas.create_line(100.0, 436.0, 500.0, 436.0, fill="#FFFFFF")
        self.canvas.create_line(100.0, 585.0, 500.0, 585.0, fill="#FFFFFF")
        self.von_image = tk.PhotoImage(file=relative_to_assets("von.png"))
        self.canvas.create_image(200.0, 510.0, image=self.von_image)
        self.bis_image = tk.PhotoImage(file=relative_to_assets("bis.png"))
        self.canvas.create_image(200.0, 660.0, image=self.bis_image)
        
        self.canvas.create_rectangle(782.0, 285.0, 1182.0, 735.0, fill="#363434", outline="#FFFFFF")
        self.geplant_image = tk.PhotoImage(file=relative_to_assets("geplant.png"))
        self.canvas.create_image(982.0, 360.0, image=self.geplant_image)
        self.canvas.create_line(782.0, 436.0, 1182.0, 436.0, fill="#FFFFFF")


        # self.canvas.create_rectangle(804.0, 437.0, 1156.0, 584.0, fill="#000000", outline="")
        # self.canvas.create_rectangle(804.0, 586.0, 1156.0, 733.0, fill="#000000", outline="")

        
        self.planer_text_image = tk.PhotoImage(file=relative_to_assets("text_planer.png"))
        self.canvas.create_image(644.0, 108.0, image=self.planer_text_image)

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

    def create_entry(self, x, y, width, height):
        entry = tk.Entry(
            self,
            bd=0,
            bg="#363434",
            fg="#FFFFFF",
            highlightthickness=0,
            justify="center",
            font=self.font
        )
        entry.place(x=x, y=y, width=width, height=height)
        return entry