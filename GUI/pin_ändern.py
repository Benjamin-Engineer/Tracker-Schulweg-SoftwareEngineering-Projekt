from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font
from PIL import Image

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from start_stop import toggle_status
from pin import change_pin

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/vboxuser/Schreibtisch/Tracker-Schulweg-SoftwareEngineering-Projekt/GUI/assets")


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)

class pin_ändernpage(tk.Frame):
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
            bg="#353333",
            height=1080,
            width=1920,
            bd=0,
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


        self.eingabe_pin_alt = self.create_entry(648.0, 276.0) 
        self.eingabe_pin_neu = self.create_entry(648.0, 434.0)
           
        self.create_button("zurück_einstellungen.png", 500.0, 804.0, 
                          lambda: self.controller.show_frame(einstellungenpage), 280, 120)
        self.create_button("bestätigen.png", 500.0, 634.0, 
                          lambda: change_pin(self.eingabe_pin_alt.get().strip(), self.eingabe_pin_neu.get().strip(), self.eingabe_pin_neu.get().strip()) ,280, 120) #einfügen von pin.py - aufruf funktion change pin -- Ruft change_pin auf, aber eingabe läuft nicht korrekt @Danny

        self.canvas.create_rectangle(-1.0, 213.0, 1280.0, 215.0, fill="#353333", outline="#FFFFFF")
        self.canvas.create_rectangle(290.0, 267.0, 990.0, 583.0, fill="#353333", outline="#FFFFFF")
        self.canvas.create_rectangle(638.0, 268.0, 639.0, 581.0, fill="#353333", outline="#FFFFFF")
        self.canvas.create_rectangle(291.0, 424.0, 988.0, 425.0, fill="#353333", outline="#FFFFFF")

    def create_entry(self, x, y):
        entry = tk.Entry(
            self,
            bd=0,
            bg="#353333",
            fg="#FFFFFF",
            highlightthickness=0,
            justify="center",
            font=self.font
        )
        entry.place(x=x, y=y, width=333.0, height=138.0)
        return entry

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

        #verknüpfen mit pin.py
        # old_pin = self.eingabe_pin_alt.get()
        # new_pin = self.eingabe_pin_neu.get()
    
        # self.eingabe_pin_alt.delete(0, tk.END)
        # self.eingabe_pin_neu.delete(0, tk.END)
