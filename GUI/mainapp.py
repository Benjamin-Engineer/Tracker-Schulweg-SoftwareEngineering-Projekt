from pathlib import Path
import tkinter as tk
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font

from start import startpage
from tracking import trackingpage
from gesperrt import gesperrtpage
from einstellungen import einstellungenpage
from pin_ändern import pin_ändernpage
from planer import planerpage
from standorte_menü import standorte_menüpage
from standorte import standortepage
from routen_menü import routen_menüpage
from routen import routenpage

OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"GUI\assets") # WINDOWS
#ASSETS_PATH = OUTPUT_PATH / Path(r"GUI/assets") # LINUX


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)

class mainappclass(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.configure(bg="#353333")
        self.resizable(False, False)
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (startpage, trackingpage, gesperrtpage, einstellungenpage, pin_ändernpage, planerpage, standorte_menüpage, standortepage, routen_menüpage, routenpage):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(startpage)
        
        
        self.timeout = 60000 #60 Sekunden

        self.bind_all("<Any-KeyPress>", self.reset_timer)
        self.bind_all("<Any-Button>", self.reset_timer)
        self.bind_all("<Motion>", self.reset_timer)        

        self.timer_id = None
        self.reset_timer()


    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()                    

    def reset_timer(self, event=None):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
        self.timer_id = self.after(self.timeout, lambda: self.show_frame(gesperrtpage))

        