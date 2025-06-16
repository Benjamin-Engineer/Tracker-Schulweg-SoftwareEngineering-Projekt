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
entsperren_image = PhotoImage(
    file=relative_to_assets("entsperren.png"))
entsperren = Button(
    image=entsperren_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("entsperren clicked"), #PIN abfrage, anschließend aufruf start
    relief="flat"
)
entsperren.place(
    x=1280.0,
    y=0.0,
    width=640.0,
    height=1080.0
)

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
    command=lambda: print("ausschalten clicked"), #ausschaltenfunktion einfügen
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
