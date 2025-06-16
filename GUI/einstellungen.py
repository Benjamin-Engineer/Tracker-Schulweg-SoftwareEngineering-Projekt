from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


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
canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    1080.0,
    fill="#353333",
    outline="")

export_image = PhotoImage(
    file=relative_to_assets("export_grau.png"))
export = Button(
    image=export_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("export clicked"), #exportfunktion einfügen
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
    command=lambda: print("einstellungen clicked"), #nichts tun?
    relief="flat"
)
einstellungen.place(
    x=1280.0,
    y=216.0,
    width=640.0,
    height=216.0
)

standorte_image = PhotoImage(
    file=relative_to_assets("standorte_grau.png"))
standorte = Button(
    image=standorte_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("standorte clicked"), #aufruf standorte_menü
    relief="flat"
)
standorte.place(
    x=1280.0,
    y=432.0,
    width=640.0,
    height=216.0
)

routen_image = PhotoImage(
    file=relative_to_assets("routen_grau.png"))
routen = Button(
    image=routen_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("routen clicked"), #aufruf routen_menü 
    relief="flat"
)
routen.place(
    x=1280.0,
    y=648.0,
    width=640.0,
    height=216.0
)

start_image = PhotoImage(
    file=relative_to_assets("start_grau.png"))
start = Button(
    image=start_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("start clicked"), #start aufrufen, tracking starten
    relief="flat"
)
start.place(
    x=1280.0,
    y=864.0,
    width=640.0,
    height=216.0
)

planer_image = PhotoImage(
    file=relative_to_assets("planer.png"))
planer = Button(
    image=planer_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("planer clicked"), #aufruf planer
    relief="flat"
)
planer.place(
    x=738.0,
    y=312.0,
    width=440.0,
    height=240.0
)

pin_ändern_image = PhotoImage(
    file=relative_to_assets("pin_ändern.png"))
pin_ändern = Button(
    image=pin_ändern_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("pin_ändern clicked"), #pin ändern aufrufen
    relief="flat"
)
pin_ändern.place(
    x=102.0,
    y=312.0,
    width=440.0,
    height=240.0
)

zurück_image = PhotoImage(
    file=relative_to_assets("zurück_einstellungen.png"))
zurück = Button(
    image=zurück_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("zurück clicked"), #start aufrufen
    relief="flat"
)
zurück.place(
    x=500.0,
    y=804.0,
    width=280.0,
    height=120.0
)
window.resizable(False, False)
window.mainloop()
