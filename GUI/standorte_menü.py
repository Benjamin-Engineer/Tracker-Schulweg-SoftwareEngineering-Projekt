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
    command=lambda: print("export clicked"), #exportfunktion aufrufen
    relief="flat"
)
export.place(
    x=1280.0,
    y=0.0,
    width=640.0,
    height=216.0
)

einstellungen_image = PhotoImage(
    file=relative_to_assets("einstellungen_grau.png"))
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
    command=lambda: print("start clicked"), # aufruf start_tracking und funktion start
    relief="flat"
)
start.place(
    x=1280.0,
    y=864.0,
    width=640.0,
    height=216.0
)

karte_image = PhotoImage(
    file=relative_to_assets("karte.png")) #platzhalter funktion karte
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
    command=lambda: print("ausschalten clicked"), #funktion ausschalten
    relief="flat"
)
ausschalten.place(
    x=51.0,
    y=929.0,
    width=100.0,
    height=100.0
)

text_standorte_image = PhotoImage(
    file=relative_to_assets("standorte.png"))
text_standorte = canvas.create_image(
    960.0,
    110.0,
    image=text_standorte_image
)

canvas.create_line(
    640.0,
    0.0,
    640.0,
    1080.0,
    fill="#FFFFFF",
    width= 4
)


canvas.create_rectangle( # standorte anzeigen
    642.0,
    218.0,
    1277.0,
    918.0,
    fill="#353333",)

canvas.create_rectangle( # karte anzeigen
    2.0,
    2.0,
    638.0,
    1078.0,
    fill="#353333",)

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
    x=819.0,
    y=930.0,
    width=280.0,
    height=97.67442321777344
)

einklappen_image= PhotoImage(
    file=relative_to_assets("einklappen.png"))
einklappen = Button(
    image=einklappen_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("einklappen clicked"), #aufruf standorte
    relief="flat"
)
einklappen.place(
    x=416.9969787597656,
    y=0.0,
    width=225.00303649902344,
    height=218.0
)
window.resizable(False, False)
window.mainloop()
