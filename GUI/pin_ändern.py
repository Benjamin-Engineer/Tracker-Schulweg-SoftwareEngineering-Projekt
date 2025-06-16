from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font

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
    command=lambda: print("export clicked"), #exportfunktion einfügen
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
    1079.0,
    fill="#353333",
    outline="#FFFFFF")

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
    command=lambda: print("standorte clicked"), #standorte aufrufen
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
    command=lambda: print("routen clicked"), #routen aufrufen
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

zurück_image = PhotoImage(
    file=relative_to_assets("zurück_einstellungen.png"))
zurück = Button(
    image=zurück_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("zurück clicked"), #einstelllungen aufrufen
    relief="flat"
)
zurück.place(
    x=500.0,
    y=804.0,
    width=280.0,
    height=120.0
)

bestätigen_image = PhotoImage(
    file=relative_to_assets("bestätigen.png"))
bestätigen = Button(
    image=bestätigen_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("bestätigen clicked"), #funktionsaufruf pin ändern, vergleich pin und speicherung neuer pin
    relief="flat"
)
bestätigen.place(
    x=500.0,
    y=634.0,
    width=280.0,
    height=120.0
)


canvas.create_rectangle(
    -1.0,
    213.0,
    1280.0,
    215.0,
    fill="#353333",
    outline="#FFFFFF")

canvas.create_rectangle(
    290.0,
    267.0,
    990.0,
    583.0,
    fill="#353333",
    outline="#FFFFFF")


eingabe_pin_alt = Entry(
    bd=0,
    bg="#353333",
    fg="#FFFFFF",
    highlightthickness=0,
    justify="center",
    # takefocus=pin,
    # validate="focus",
    # invalidcommand=print("wrong pin, überschreibung nicht erlaubt"),  verknüpfung menüfunktion pin ändern
    # validatecommand=print("correct pin, überschreibung erlaubt")  verknüpfung menüfunktion pin ändern
)

eingabe_pin_alt.place(
    x=648.0,
    y=434.0,
    width=333.0,
    height=138.0
)

eingabe_pin_neu = Entry(
    bd=0,
    bg="#353333",
    fg="#FFFFFF",
    highlightthickness=0,
    justify="center"
)
eingabe_pin_neu.place(
    x=648.0,
    y=276.0,
    width=333.0,
    height=138.0
)

canvas.create_rectangle(
    638.0,
    268.0,
    639.0,
    581.0,
    fill="#353333",
    outline="#FFFFFF")

canvas.create_rectangle(
    291.0,
    424.0,
    988.0,
    425.0000000000002,
    fill="#353333",
    outline="#FFFFFF")
window.resizable(False, False)
window.mainloop()
