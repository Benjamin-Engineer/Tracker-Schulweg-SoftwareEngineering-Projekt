from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font
from PIL import Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/GUI/assets")


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
                           lambda: self.controller.show_frame(startpage), 640, 216) #funktion einfügen start tracking
        

        self.pin_ändern_text_image = tk.PhotoImage(file=relative_to_assets("text_pin_ändern.png"))
        self.canvas.create_image(644.0, 108.0, image=self.pin_ändern_text_image)
        self.canvas.create_rectangle(0.0, 214.0, 1280.0, 218.0, fill="#FFFFFF", outline="")


        self.eingabe_pin_alt = self.create_entry(648.0, 434.0)
        self.eingabe_pin_neu = self.create_entry(648.0, 276.0)

        self.create_button("zurück_einstellungen.png", 500.0, 804.0, 
                          lambda: self.controller.show_frame(einstellungenpage), 280, 120)
        self.create_button("bestätigen.png", 500.0, 634.0, lambda: print("bestätigen clicked"), 280, 120) #einfügen von pin.py - aufruf funktion change pin

        self.canvas.create_rectangle(290.0, 267.0, 990.0, 583.0, fill="#363434", outline="#FFFFFF")
        self.canvas.create_line(640.0, 267.0, 640.0, 583.0, fill="#FFFFFF")
        self.canvas.create_line(290.0, 425.0, 990.0, 425.0, fill="#FFFFFF")
        self.alte_pin_image = tk.PhotoImage(file=relative_to_assets("alte_pin.png"))
        self.canvas.create_image(470.0, 345.0, image=self.alte_pin_image)
        self.neue_pin_image = tk.PhotoImage(file=relative_to_assets("neue_pin.png"))
        self.canvas.create_image(470.0, 505.0, image=self.neue_pin_image)


    def create_entry(self, x, y):
        entry = tk.Entry(
            self,
            bd=0,
            bg="#363434",
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
            relief="flat",
            background="#363434"
        )
        btn.image = img
        btn.place(x=x, y=y, width=width, height=height)
        return btn

        #verknüpfen mit pin.py
        # old_pin = self.eingabe_pin_alt.get()
        # new_pin = self.eingabe_pin_neu.get()
    
        # self.eingabe_pin_alt.delete(0, tk.END)
        # self.eingabe_pin_neu.delete(0, tk.END)