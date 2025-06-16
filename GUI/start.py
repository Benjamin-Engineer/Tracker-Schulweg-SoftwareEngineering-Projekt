from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/vboxuser/Schreibtisch/Tracker-Schulweg-SoftwareEngineering-Projekt/GUI/assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1920x1080")
window.configure(bg = "#353333")


canvas = Canvas(
    window,
    bg = "#353333",
    height = 1080,
    width = 1920,
    bd = 2,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
export_image = PhotoImage(
    file=relative_to_assets("export.png"))
export = Button(
    image=export_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Export clicked"), #Funktionsaufruf Export einfügen
    relief="flat"
)
export.place(
    x=1280.0,
    y=0.0,
    width=640.0,
    height=216.0
)

einstellungen_image = PhotoImage(
    file=relative_to_assets("einstellungen.png"))
einstellungen = Button(
    image=einstellungen_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Einstellungen clicked"), #Aufruf Screen Einstellungen
    relief="flat"
)
einstellungen.place(
    x=1280.0,
    y=216.0,
    width=640.0,
    height=216.0
)

standorte_image = PhotoImage(
    file=relative_to_assets("standorte.png"))
standorte = Button(
    image=standorte_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("standorte clicked"), #Aufruf Standorte
    relief="flat"
)
standorte.place(
    x=1280.0,
    y=432.0,
    width=640.0,
    height=216.0
)

routen_image = PhotoImage(
    file=relative_to_assets("routen.png"))
routen = Button(
    image=routen_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("routen clicked"), #Aufruf Routen
    relief="flat"
)
routen.place(
    x=1280.0,
    y=648.0,
    width=640.0,
    height=216.0
)

start_image = PhotoImage(
    file=relative_to_assets("start.png"))
start = Button(
    image=start_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("start clicked"), #start tracking aufrufen
    relief="flat"
)
start.place(
    x=1280.0,
    y=864.0,
    width=640.0,
    height=216.0
)

#Platzhalter für funktion der Karte

karte_image = PhotoImage(
    file=relative_to_assets("karte.png"))
karte = canvas.create_image(
    640.0,
    540.0,
    image=karte_image
)

ausschalten_image = PhotoImage(
    file=relative_to_assets("ausschalten.png"))
ausschalten = Button(
    image=ausschalten_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("ausschalten clicked"), #ausschalten Funnktion einfügen
    relief="flat"
)
ausschalten.place(
    x=51.0,
    y=929.0,
    width=100.0,
    height=100.0
)
window.resizable(False, False)
window.mainloop()
