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

routen_img_image = PhotoImage(
    file=relative_to_assets("routen.png"))
routen_img = Button(
    image=routen_img_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("routen_img clicked"), #nichts tun 
    relief="flat"
)
routen_img.place(
    x=640.0,
    y=0.0,
    width=640.0,
    height=216.0
)

canvas.create_line(
    640.0,
    0.0,
    640.0,
    1080.0,
    fill="#FFFFFF",
    width= 4
)

export_image = PhotoImage(
    file=relative_to_assets("export_grau.png"))
export = Button(
    image=export_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("export clicked"), #exportfunkltion einfügen
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
    file=relative_to_assets("standorte_grau.png"))
standorte = Button(
    image=standorte_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("standorte clicked"), #standorte_menü aufrufen
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
    command=lambda: print("routen clicked"), #nichts tun?
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
    command=lambda: print("ausschalten clicked"), #ausschalten-funktion aufrufen
    relief="flat"
)
ausschalten.place(
    x=51.0,
    y=929.0,
    width=100.0,
    height=100.0
)

canvas.create_rectangle(
    638.0,
    0.0,
    1278.0,
    1078.0,
    fill="#353333",
    outline="#FFFFFF")

routen_löschen_image = PhotoImage(
    file=relative_to_assets("routen_löschen.png"))
routen_löschen = Button(
    image=routen_löschen_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("routen löschen clicked"), #einzelne oder alle routen löschen?
    relief="flat"
)
routen_löschen.place(
    x=819.0,
    y=782.0,
    width=280.0,
    height=97.67442321777344
)

canvas.create_rectangle(
    642.0,
    218.0,
    1278.0,
    773.0,
    fill="#000000",
    outline="")

einklappen_image = PhotoImage(
    file=relative_to_assets("einklappen.png"))
einklappen = Button(
    image=einklappen_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("einklappen clicked"), #routen aufrufen
    relief="flat"
)
einklappen.place(
    x=416.9969787597656,
    y=0.0,
    width=225.00303649902344,
    height=218.0
)

zurück_image = PhotoImage(
    file=relative_to_assets("zurück.png"))
zurück = Button(
    image=zurück_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("zurück clicked"), #start aufrufen
    relief="flat"
)
zurück.place(
    x=819.0,
    y=930.0,
    width=280.0,
    height=97.67442321777344
)
window.resizable(False, False)
window.mainloop()
