from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font
from PIL import Image

import sys
import os
import json
from datetime import datetime
from tkinter import ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shutdown import system_shutdown

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/GUI/assets")


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)

class routen_menüpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        from einstellungen import einstellungenpage
        from standorte_menü import standorte_menüpage
        from routen import routenpage
        from start import startpage
        self.controller = controller
        
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
                           lambda: print("Export clicked"), 640, 216) #einfügen exportfunktion
        self.create_button("einstellungen_grau.png", 1280, 216, 
                           lambda: self.controller.show_frame(einstellungenpage), 640, 216)
        self.create_button("standorte_grau.png", 1280, 432, 
                           lambda: self.controller.show_frame(standorte_menüpage), 640, 216)
        self.create_button("routen.png", 1280, 648, 
                           lambda: print("Routen clicked"), 640, 216)
        self.create_button("start_grau.png", 1280, 864, 
                           lambda: self.controller.show_frame(startpage), 640, 216) #funktion einfügen start tracking

        self.create_button("routen.png", 640.0, 0.0, 
                          lambda: print("Routen clicked"), 640.0, 216.0)

        self.canvas.create_line(640.0, 0.0, 640.0, 1080.0, fill="#FFFFFF", width=4)

        # platzhalter karte - Meeting mit Hossein/Mohammed
        self.karte_image = tk.PhotoImage(file=relative_to_assets("karte.png"))
        self.canvas.create_image(640.0, 540.0, image=self.karte_image)

        self.canvas.create_rectangle(638.0, 0.0, 1278.0, 1078.0, fill="#363434", outline="#FFFFFF")

        # Routen-Liste Container anstatt schwarzer Platzhalter
        self.setup_routes_list()

        self.create_button("ausschalten.png", 51.0, 929.0,
                          lambda: system_shutdown(), 100.0, 100.0) #funktion ausschalten einfügen

        self.create_button("routen_löschen.png", 819.0, 782.0,
                          lambda: self.delete_selected_route(), 280.0, 97.67442321777344)

        self.create_button("einklappen.png", 425.0, 0.0,
                          lambda: self.view_selected_route(), 215.0, 216.0)

        self.create_button("zurück.png", 819.0, 930.0,
                          lambda: self.controller.show_frame(startpage), 280.0, 97.67442321777344)
        
        self.canvas.create_rectangle(638.0, 216.0, 642.0, 1080.0, fill="#FFFFFF", outline="")

        # Lade die Routen für das aktuelle Datum
        self.load_routes()

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

    def setup_routes_list(self):
        """Erstellt die Routen-Liste mit Scrollbar"""
        # Frame für die Routen-Liste
        list_frame = tk.Frame(self, bg="#000000")
        list_frame.place(x=642, y=218, width=636, height=555)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox für die Routen
        self.routes_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg="#000000",
            fg="#FFFFFF",
            selectbackground="#555555",
            selectforeground="#FFFFFF",
            font=("Arial", 12),
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        self.routes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.routes_listbox.yview)
        
        # Titel für die Liste
        title_label = tk.Label(
            self,
            text=f"Routen vom {datetime.now().strftime('%Y-%m-%d')}",
            bg="#363434",
            fg="#FFFFFF",
            font=("Arial", 14, "bold")
        )
        title_label.place(x=642, y=190)

    def load_routes(self):
        """Lädt die verfügbaren Routen für das aktuelle Datum"""
        try:
            # Aktuelles Datum für Ordnername
            current_date = datetime.now().strftime('%Y-%m-%d')
            routes_dir = Path(__file__).parent.parent / current_date
            
            self.routes_listbox.delete(0, tk.END)
            self.route_files = []
            
            if routes_dir.exists():
                # Alle JSON-Dateien im Datumsordner finden
                json_files = list(routes_dir.glob("*.json"))
                
                for json_file in sorted(json_files):
                    # Route-Information aus JSON-Datei laden
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            route_data = json.load(f)
                        
                        # Routeninformationen anzeigen
                        route_name = json_file.stem  # Dateiname ohne Endung
                        num_points = len(route_data)
                        
                        # Start- und Endzeit extrahieren
                        if route_data:
                            start_time = route_data[0].get('time', 'Unbekannt')
                            end_time = route_data[-1].get('time', 'Unbekannt')
                            
                            # Formatierte Anzeige
                            display_text = f"{route_name} ({num_points} Punkte)"
                            if start_time != 'Unbekannt':
                                display_text += f" - {start_time[:19]}"
                        else:
                            display_text = f"{route_name} (Leere Route)"
                        
                        self.routes_listbox.insert(tk.END, display_text)
                        self.route_files.append(str(json_file))
                        
                    except (json.JSONDecodeError, Exception) as e:
                        # Fehlerhafte Dateien überspringen
                        self.routes_listbox.insert(tk.END, f"{json_file.name} (Fehler beim Laden)")
                        self.route_files.append(None)
                
                if not json_files:
                    self.routes_listbox.insert(tk.END, "Keine Routen für heute verfügbar")
            else:
                self.routes_listbox.insert(tk.END, "Ordner für heutiges Datum nicht gefunden")
                
        except Exception as e:
            self.routes_listbox.insert(tk.END, f"Fehler beim Laden der Routen: {str(e)}")

    def view_selected_route(self):
        """Zeigt die ausgewählte Route in der Kartenseite an"""
        selection = self.routes_listbox.curselection()
        if selection and len(self.route_files) > selection[0]:
            route_file = self.route_files[selection[0]]
            if route_file:
                # Zur Routen-Ansichtsseite wechseln und Route anzeigen
                from routen import routenpage
                routes_page = None
                
                # routenpage-Instanz finden
                for frame_name, frame in self.controller.frames.items():
                    if isinstance(frame, routenpage):
                        routes_page = frame
                        break
                
                if routes_page:
                    routes_page.display_route(route_file)
                    self.controller.show_frame(routenpage)
            else:
                print("Ausgewählte Route kann nicht geladen werden")
        else:
            print("Bitte wählen Sie eine Route aus")

    def delete_selected_route(self):
        """Löscht die ausgewählte Route"""
        selection = self.routes_listbox.curselection()
        if selection and len(self.route_files) > selection[0]:
            route_file = self.route_files[selection[0]]
            if route_file:
                try:
                    # Route-Datei löschen
                    os.remove(route_file)
                    print(f"Route gelöscht: {route_file}")
                    
                    # Liste aktualisieren
                    self.load_routes()
                except Exception as e:
                    print(f"Fehler beim Löschen der Route: {str(e)}")
            else:
                print("Ausgewählte Route kann nicht gelöscht werden")
        else:
            print("Bitte wählen Sie eine Route zum Löschen aus")
