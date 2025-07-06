from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, font
from PIL import Image

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shutdown import system_shutdown
from map_widget import MapWidget

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/GUI/assets")


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)


class standortepage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        from standorte_menü import standorte_menüpage
        from start import startpage
        self.controller = controller
        
        self.canvas = tk.Canvas(
            self,
            bg="#363434",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Initialize and place the map widget for location viewing
        self.map_widget = MapWidget(self, width=1280, height=1080)
        self.map_widget.place(x=0, y=0)

        self.create_button("ausschalten.png", 51.0, 929.0, 
                        lambda: system_shutdown(), 100.0, 100.0) #funktion ausschalten einfügen

        self.canvas.create_rectangle(
            1278.0, 0.0, 1919.0, 1079.0,
            fill="#363434", outline="#FFFFFF"
        )

        self.create_button("standorte.png", 1280.0, 0.0,
                         lambda: print("Standorte clicked"), 640.0, 216.0) #nichts tun

        self.create_button("ausklappen.png", 1071.0, 0.0,
                         lambda: self.controller.show_frame(standorte_menüpage), 
                         208.0, 217.0)
        self.canvas.create_rectangle(1278.0, -2.0, 1282.0, 1080.0, fill="#FFFFFF", outline="")

        # Kompakte Standorte-Liste für eingeklappte Ansicht
        # Hintergrund für die Liste
        self.canvas.create_rectangle(
            1282.0, 218.0, 1918.0, 918.0,
            fill="#363434", outline=""
        )
        
        # Titel für die kompakte Liste
        self.canvas.create_text(
            1600.0, 240.0,
            text="Standorte",
            fill="#FFFFFF",
            font=("Inter", 16, "bold"),
            anchor="center"
        )
        
        list_frame = tk.Frame(self, bg="#363434")
        list_frame.place(x=1285, y=260, width=630, height=655)  # Etwas kleiner wegen Titel
        
        # Vertikale Scrollbar (identisch zur ursprünglichen Liste)
        v_scrollbar = tk.Scrollbar(list_frame, orient="vertical", bg="#363434")
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Horizontale Scrollbar (identisch zur ursprünglichen Liste)
        h_scrollbar = tk.Scrollbar(list_frame, orient="horizontal", bg="#363434")
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Kompakte Standorte-Liste hinzufügen (identisches Styling)
        self.standorte_listbox = tk.Listbox(
            list_frame,
            bg="#363434",
            fg="#FFFFFF",
            font=("Inter", 24),  # Identische Schriftgröße wie ursprüngliche Liste
            selectbackground="#555555",
            selectforeground="#FFFFFF",
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        self.standorte_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars konfigurieren (identisch zur ursprünglichen Liste)
        v_scrollbar.config(command=self.standorte_listbox.yview)
        h_scrollbar.config(command=self.standorte_listbox.xview)
        
        # Event-Handler für Standort-Auswahl hinzufügen
        self.standorte_listbox.bind('<<ListboxSelect>>', self.on_standort_select)
        
        # Mausrad-Unterstützung hinzufügen (identisch zur ursprünglichen Liste)
        self.standorte_listbox.bind("<MouseWheel>", self._on_mousewheel)
        self.standorte_listbox.bind("<Shift-MouseWheel>", self._on_horizontal_mousewheel)
        
        # Standorte laden und speichern für Referenz
        self.standorte_data = []  # Speichert die Original-Standortdaten
        self.current_marker = None  # Speichert den aktuellen Marker
        self.load_standorte()

        self.create_button("zurück.png", 1460.0, 930.0,
                         lambda: self.controller.show_frame(startpage), 
                         280.0, 97.67442321777344)

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

    def _on_mousewheel(self, event):
        """Handle vertical mouse wheel scrolling"""
        self.standorte_listbox.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_horizontal_mousewheel(self, event):
        """Handle horizontal mouse wheel scrolling (Shift + mouse wheel)"""
        self.standorte_listbox.xview_scroll(int(-1*(event.delta/120)), "units")

    def load_standorte(self):
        """Lade alle Standorte aus dem Standorte-Ordner (identisch zur ursprünglichen Liste)"""
        try:
            import dateifunktionen
            standorte = dateifunktionen.get_standorte()
            
            # Liste leeren
            self.standorte_listbox.delete(0, tk.END)
            self.standorte_data = []  # Original-Daten auch leeren
            
            if not standorte:
                self.standorte_listbox.insert(tk.END, "Keine Standorte gefunden")
                return
            
            # Standorte anzeigen (identisch zur ursprünglichen Liste)
            for location, custom_name, timestamp in standorte:
                if custom_name and custom_name != location:
                    # Benutzer hat einen eigenen Namen vergeben
                    display_text = f"{custom_name} ({location}) - {timestamp}"
                else:
                    # Kein benutzerdefinierter Name -> "Längerer Aufenthalt" verwenden
                    display_text = f"Längerer Aufenthalt ({location}) - {timestamp}"
                self.standorte_listbox.insert(tk.END, display_text)
                
                # Original-Daten für spätere Verwendung speichern
                self.standorte_data.append((location, custom_name, timestamp))
            
            print(f"Standorte-Eingeklappt: {len(standorte)} Standorte geladen")
            
        except Exception as e:
            self.standorte_listbox.delete(0, tk.END)
            self.standorte_listbox.insert(tk.END, f"Fehler beim Laden: {e}")
            self.standorte_data = []
            print(f"Fehler beim Laden der Standorte: {e}")

    def on_standort_select(self, event):
        """Event-Handler für Standort-Auswahl in der kompakten Liste"""
        try:
            # Aktuelle Auswahl abrufen
            selection = self.standorte_listbox.curselection()
            if not selection:
                return
            
            index = selection[0]
            
            # Prüfen ob gültige Daten vorhanden sind
            if index >= len(self.standorte_data):
                print("Fehler: Ungültiger Standort-Index")
                return
            
            # Standort-Daten abrufen
            location, custom_name, timestamp = self.standorte_data[index]
            
            # Koordinaten aus location-String extrahieren
            coords = self.parse_coordinates(location)
            if coords:
                lat, lon = coords
                
                # Vorherigen Marker löschen, falls vorhanden
                if self.current_marker:
                    try:
                        self.current_marker.delete()
                        print("Vorheriger Marker gelöscht")
                    except Exception as e:
                        print(f"Fehler beim Löschen des vorherigen Markers: {e}")
                
                # Alle Marker löschen (als zusätzliche Sicherheit)
                try:
                    self.map_widget.map_widget.delete_all_marker()
                    print("Alle Marker gelöscht")
                except Exception as e:
                    print(f"Fehler beim Löschen aller Marker: {e}")
                
                # Karte auf Standort zentrieren
                self.map_widget.map_widget.set_position(lat, lon)
                
                # Neuen Marker für den Standort setzen
                if custom_name and custom_name != location:
                    marker_text = custom_name
                else:
                    marker_text = "Längerer Aufenthalt"
                self.current_marker = self.map_widget.map_widget.set_marker(lat, lon, text=marker_text)
                
                # Marker-Farbe setzen (grün für gespeicherte Standorte)
                if hasattr(self.current_marker, 'marker_color_circle'):
                    self.current_marker.marker_color_circle = "green"
                
                print(f"Standort auf Karte angezeigt: {lat:.6f}, {lon:.6f} - {marker_text}")
            else:
                print(f"Fehler: Konnte Koordinaten nicht extrahieren aus '{location}'")
                
        except Exception as e:
            print(f"Fehler bei Standort-Auswahl: {e}")
    
    def parse_coordinates(self, location_str):
        """Extrahiert Lat/Lon Koordinaten aus dem Location-String"""
        try:
            # Format: "50.123456 7.123456" oder ähnlich
            parts = location_str.strip().split()
            if len(parts) >= 2:
                lat = float(parts[0])
                lon = float(parts[1])
                return (lat, lon)
        except (ValueError, IndexError) as e:
            print(f"Fehler beim Parsen der Koordinaten '{location_str}': {e}")
        return None

    def refresh_standorte(self):
        """Aktualisiere die Standorte-Liste (für externe Aufrufe)"""
        self.load_standorte()

    def on_show(self):
        """Wird aufgerufen, wenn die eingeklappte Seite angezeigt wird"""
        self.load_standorte()
        # Alle vorherigen Marker löschen
        try:
            self.map_widget.map_widget.delete_all_marker()
            self.current_marker = None
            print("Alle Marker beim Laden der eingeklappten Seite gelöscht")
        except Exception as e:
            print(f"Fehler beim Löschen der Marker: {e}")
        
        # Karte auf Standard-Position setzen (Bonn)
        try:
            self.map_widget.map_widget.set_position(50.7374, 7.0982)  # Bonn Zentrum
        except Exception as e:
            print(f"Fehler beim Setzen der Standard-Kartenposition: {e}")

    def display_location(self, location_file):
        """
        Display a specific location on the map
        """
        if location_file and self.map_widget:
            self.map_widget.standort(location_file)
