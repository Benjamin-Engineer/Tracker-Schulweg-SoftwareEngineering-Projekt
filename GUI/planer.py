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
export_image = PhotoImage(
    file=relative_to_assets("export_grau.png"))
export = Button(
    image=export_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("export clicked"), #exportfunktio aufrufen
    relief="flat"
)
export.place(
    x=1280.0,
    y=0.0,
    width=640.0,
    height=216.0
)

canvas.create_rectangle(
    0.0,
    0.0,
    1282.0,
    1080.0,
    fill="#353333",
    outline="")

einstellungen_image = PhotoImage(
    file=relative_to_assets("einstellungen.png"))
einstellungen = Button(
    image=einstellungen_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("einstellungen clicked"), #einstellungen aufrufen
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
    command=lambda: print("standorte clicked"), #aufruf standorte
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
    command=lambda: print("routen clicked"), #aufruf routen
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
    command=lambda: print("start clicked"), #aufruf start, start tracking
    relief="flat"
)
start.place(
    x=1280.0,
    y=864.0,
    width=640.0,
    height=216.0
)

zurück_image = PhotoImage(
    file=relative_to_assets("zurück_einstellungen.png"))
zurück = Button(
    image=zurück_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("zurück clicked"), #aufruf einstellungen
    relief="flat"
)
zurück.place(
    x=500.0,
    y=804.0,
    width=280.0,
    height=120.0
)

canvas.create_rectangle(
    -1.0,
    213.0,
    1280.0,
    215.0,
    fill="#353333",
    outline="")

canvas.create_image(
    308.0,
    0.0,
    972.0,
    216.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    100.0,
    285.0,
    500.0,
    735.0,
    fill="#353333",
    outline="")

eingabe_von = Entry(
    bd=0,
    bg="#353333",
    fg="#FFFFFF",
    highlightthickness=0,
    justify="center"
)
eingabe_von.place(
    x=302.0,
    y=586.0,
    width=190.0,
    height=137.0
)

eingabe_bis = Entry(
    bd=0,
    bg="#353333",
    fg="#FFFFFF",
    highlightthickness=0,
    justify="center"
)
eingabe_bis.place(
    x=302.0,
    y=437.0,
    width=196.0,
    height=145.0
)

hinzufügen_image = PhotoImage(
    file=relative_to_assets("hinzufügen.png"))
hinzufügen = Button(
    image=hinzufügen_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("hinzufügen clicked"), #einfügen funktion schreiben von trackingdaten, überprüfung ob etwas in eingabe ist, überprüfung überschneidung
    relief="flat"
)
hinzufügen.place(
    x=109.0,
    y=294.0,
    width=382.0,
    height=141.0
)

canvas.create_rectangle(
    782.0,
    285.0,
    1182.0,
    735.0,
    fill="#353333",
    outline="")

canvas.create_rectangle(
    804.0,
    437.0,
    1156.0,
    584.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    804.0,
    586.0,
    1156.0,
    733.0,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()
