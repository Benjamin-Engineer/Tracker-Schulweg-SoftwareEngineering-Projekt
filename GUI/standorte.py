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
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

karte_image = PhotoImage(
    file=relative_to_assets("karte.png")) #platzhalter kartenfunktion
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
    command=lambda: print("ausschalten clicked"),
    relief="flat"
)
ausschalten.place(
    x=51.0,
    y=929.0,
    width=100.0,
    height=100.0
)

canvas.create_rectangle(
    1278.0,
    0.0,
    1919.0,
    1079.0,
    fill="#353333",
    outline="#FFFFFF")

canvas.place(x = 0, y = 0)
standorte_image = PhotoImage(
    file=relative_to_assets("standorte.png"))
standorte = Button(
    image=standorte_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("standorte clicked"), #nichts tun?
    relief="flat"
)
standorte.place(
    x=1280.0,
    y=0.0,
    width=640.0,
    height=216.0
)

ausklappen_image = PhotoImage(
    file=relative_to_assets("ausklappen.png"))
ausklappen = Button(
    image=ausklappen_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("ausklappen clicked"), #aufruf standorte_menü
    relief="flat"
)
ausklappen.place(
    x=1071.0,
    y=0.0,
    width=218.0,
    height=218.0
)

canvas.create_rectangle(
    1282.0,
    218.0,
    1918.0,
    918.0,
    fill="#000000",
    outline="")

zurück_image = PhotoImage(
    file=relative_to_assets("zurück.png"))
zurück = Button(
    image=zurück_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("zurück clicked"), #aufruf start
    relief="flat"
)
zurück.place(
    x=1460.0,
    y=930.0,
    width=280.0,
    height=97.67442321777344
)
window.resizable(False, False)
window.mainloop()
