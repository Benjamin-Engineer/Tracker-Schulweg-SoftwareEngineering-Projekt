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

from start_stop import toggle_status
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
                           lambda: toggle_status(), 640, 216) #funktion einfügen start tracking

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
                          lambda: self.controller.show_frame(startpage), 215.0, 216.0)

        self.create_button("zurück.png", 819.0, 930.0,
                          lambda: self.controller.show_frame(startpage), 280.0, 97.67442321777344)
        
        self.canvas.create_rectangle(638.0, 216.0, 642.0, 1080.0, fill="#FFFFFF", outline="")

        # Lade die Routen für das aktuelle Datum
        self.load_routes()

    def _on_mousewheel(self, event):
        """Handle vertical mouse wheel scrolling"""
        self.routes_listbox.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_horizontal_mousewheel(self, event):
        """Handle horizontal mouse wheel scrolling (Shift + mouse wheel)"""
        self.routes_listbox.xview_scroll(int(-1*(event.delta/120)), "units")

    def on_show(self):
        """Wird aufgerufen, wenn die Seite angezeigt wird"""
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
        list_frame = tk.Frame(self, bg="#363434")
        list_frame.place(x=642, y=218, width=636, height=555)
        
        # Vertikale Scrollbar
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Horizontale Scrollbar
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal")
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Listbox für die Routen
        self.routes_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            bg="#363434",
            fg="#FFFFFF",
            selectbackground="#555555",
            selectforeground="#FFFFFF",
            font=("Inter", 24),
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        self.routes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars konfigurieren
        v_scrollbar.config(command=self.routes_listbox.yview)
        h_scrollbar.config(command=self.routes_listbox.xview)
        
        # Event-Handler für Auswahl in der Liste hinzufügen
        self.routes_listbox.bind('<<ListboxSelect>>', self.on_route_select)
        
        # Mausrad-Unterstützung hinzufügen
        self.routes_listbox.bind("<MouseWheel>", self._on_mousewheel)
        self.routes_listbox.bind("<Shift-MouseWheel>", self._on_horizontal_mousewheel)
        
        # Titel für die Liste (als Attribut speichern)
        self.title_label = tk.Label(
            self,
            text="Lade Routen...",
            bg="#363434",
            fg="#FFFFFF",
            font=("Arial", 14, "bold")
        )
        self.title_label.place(x=642, y=190)

    def load_routes(self):
        """Lädt alle verfügbaren Routen, chronologisch sortiert (neueste zuerst)"""
        try:
            # Pfad zum übergeordneten Verzeichnis (wo sich die Datumsordner befinden)
            base_dir = Path(__file__).parent.parent
            
            self.routes_listbox.delete(0, tk.END)
            self.route_files = []
            
            # Lade alle Routen chronologisch sortiert
            import sys
            if str(base_dir) not in sys.path:
                sys.path.append(str(base_dir))
            
            try:
                import dateifunktionen
                all_routes = dateifunktionen.get_all_routes_sorted(str(base_dir))
                
                if all_routes:
                    print(f"DEBUG: Gefundene Routen: {len(all_routes)}")
                    for i, route_info in enumerate(all_routes):
                        display_name = route_info['display_name']
                        file_path = route_info['file_path']  # Sollte bereits absolut sein
                        
                        print(f"DEBUG: Route {i}: {display_name}")
                        print(f"DEBUG: Pfad: {file_path}")
                        print(f"DEBUG: Datei existiert: {os.path.exists(file_path)}")
                        
                        self.routes_listbox.insert(tk.END, display_name)
                        self.route_files.append(file_path)
                        
                    # Aktualisiere den Titel
                    if hasattr(self, 'title_label'):
                        self.title_label.config(text=f"Alle Routen ({len(all_routes)} gefunden)")
                else:
                    self.routes_listbox.insert(tk.END, "Keine Routen verfügbar")
                    if hasattr(self, 'title_label'):
                        self.title_label.config(text="Keine Routen verfügbar")
                        
            except ImportError as ie:
                error_msg = f"Import-Fehler: {str(ie)}"
                print(f"DEBUG: {error_msg}")
                self.routes_listbox.insert(tk.END, error_msg)
                
        except Exception as e:
            error_msg = f"Fehler beim Laden der Routen: {str(e)}"
            print(f"DEBUG: {error_msg}")
            self.routes_listbox.insert(tk.END, error_msg)
            import traceback
            traceback.print_exc()

    def on_route_select(self, event):
        """Event-Handler für Route-Auswahl in der Liste"""
        self.view_selected_route()

    def view_selected_route(self):
        """Zeigt die ausgewählte Route in der Kartenseite an"""
        selection = self.routes_listbox.curselection()
        print(f"DEBUG: Selection: {selection}")
        print(f"DEBUG: Anzahl route_files: {len(self.route_files) if hasattr(self, 'route_files') else 'Nicht initialisiert'}")
        
        if selection and hasattr(self, 'route_files') and len(self.route_files) > selection[0]:
            route_file = self.route_files[selection[0]]
            selected_text = self.routes_listbox.get(selection[0])
            print(f"DEBUG: Ausgewählte Route: {selected_text}")
            print(f"DEBUG: Route-Datei: {route_file}")
            
            if route_file and os.path.exists(route_file):
                # Zur Routen-Ansichtsseite wechseln und Route anzeigen
                from routen import routenpage
                routes_page = None
                
                # routenpage-Instanz finden
                for frame_name, frame in self.controller.frames.items():
                    if isinstance(frame, routenpage):
                        routes_page = frame
                        break
                
                if routes_page:
                    print(f"DEBUG: Zeige Route an: {route_file}")
                    # Erst zur Seite wechseln
                    self.controller.show_frame(routenpage)
                    # Dann mit after() die Route nach dem Frame-Switch laden
                    self.after(100, lambda: routes_page.display_route(route_file))
                else:
                    print("DEBUG: Routenpage nicht gefunden")
            else:
                if not route_file:
                    print("DEBUG: Route-Datei ist None")
                else:
                    print(f"DEBUG: Route-Datei existiert nicht: {route_file}")
        else:
            if not selection:
                print("DEBUG: Keine Route ausgewählt")
            elif not hasattr(self, 'route_files'):
                print("DEBUG: route_files Attribut nicht vorhanden")
            else:
                print(f"DEBUG: Selection Index außerhalb des Bereichs: {selection[0]} >= {len(self.route_files)}")

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
