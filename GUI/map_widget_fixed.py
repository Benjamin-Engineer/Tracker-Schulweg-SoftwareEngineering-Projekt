import tkinter as tk
import tkintermapview  
import os
import sys

# Add parent directory to path to access dateifunktionen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import dateifunktionen


class MapWidget:
    def __init__(self, parent, width=1280, height=1080):
        """
        Map widget that can be embedded in other tkinter applications
        """
        self.parent = parent
        
        # Create the map widget
        self.map_widget = tkintermapview.TkinterMapView(
            parent, 
            width=width, 
            height=height, 
            corner_radius=0
        )
        
        # Set initial position (Bonn)
        self.map_widget.set_position(50.7374, 7.0982)
        self.map_widget.set_zoom(15)
        
        # Store markers for cleanup
        self.markers = []
        self.current_path = None
        self.route_points = []

    def place(self, x=0, y=0):
        """Place the map widget at the specified position"""
        self.map_widget.place(x=x, y=y)

    def pack(self, **kwargs):
        """Pack the map widget"""
        self.map_widget.pack(**kwargs)

    def grid(self, **kwargs):
        """Grid the map widget"""
        self.map_widget.grid(**kwargs)

    def clear_map(self):
        """Clear all markers and paths from the map"""
        print("DEBUG MapWidget: Lösche Karte")
        
        # Clear all markers
        for marker in self.markers:
            marker.delete()
        self.markers.clear()
        
        # Clear path
        if self.current_path:
            self.map_widget.delete_path(self.current_path)
            self.current_path = None
            
        # Clear route points
        self.route_points = []
        
        print("DEBUG MapWidget: Karte geleert")

    def route(self, routendatei):
        """Zeigt die Route einer Routendatei samt all ihrer Standorte an. Bei Live Tracking wiederholt aufrufen zum aktualisieren."""
        try:
            print(f"DEBUG MapWidget: Lade Route von {routendatei}")
            self.clear_map()
            
            # Prüfe ob Datei existiert
            if not os.path.exists(routendatei):
                print(f"DEBUG MapWidget: Route-Datei existiert nicht: {routendatei}")
                return
            
            self.route_points = dateifunktionen.routendatei_zu_liste(routendatei)
            print(f"DEBUG MapWidget: {len(self.route_points) if self.route_points else 0} Route-Punkte geladen")
            
            if self.route_points:
                # Erstelle Pfad
                self.current_path = self.map_widget.set_path(self.route_points)
                print(f"DEBUG MapWidget: Pfad mit {len(self.route_points)} Punkten erstellt")
                
                # Zeige Standorte
                self.standorte(routendatei)
                
                # Positioniere Karte auf den Mittelpunkt der Route
                if len(self.route_points) > 0:
                    # Berechne Mittelpunkt der Route
                    center_lat = sum(point[0] for point in self.route_points) / len(self.route_points)
                    center_lon = sum(point[1] for point in self.route_points) / len(self.route_points)
                    
                    # Setze Position und Zoom
                    self.map_widget.set_position(center_lat, center_lon)
                    
                    # Berechne geeigneten Zoom basierend auf Route-Ausdehnung
                    if len(self.route_points) > 1:
                        lat_range = max(point[0] for point in self.route_points) - min(point[0] for point in self.route_points)
                        lon_range = max(point[1] for point in self.route_points) - min(point[1] for point in self.route_points)
                        
                        # Einfache Zoom-Berechnung basierend auf der Ausdehnung
                        max_range = max(lat_range, lon_range)
                        if max_range > 0.01:  # Große Route
                            zoom = 12
                        elif max_range > 0.005:  # Mittlere Route
                            zoom = 14
                        else:  # Kleine Route
                            zoom = 16
                        
                        self.map_widget.set_zoom(zoom)
                        print(f"DEBUG MapWidget: Karte zentriert auf ({center_lat:.6f}, {center_lon:.6f}) mit Zoom {zoom}")
                    else:
                        print(f"DEBUG MapWidget: Karte positioniert auf einzelnen Punkt ({center_lat:.6f}, {center_lon:.6f})")
                else:
                    print("DEBUG MapWidget: Nur ein Route-Punkt vorhanden")
            else:
                print("DEBUG MapWidget: Keine Route-Punkte gefunden")
        except Exception as e:
            print(f"DEBUG MapWidget: Fehler beim Anzeigen der Route: {e}")
            import traceback
            traceback.print_exc()

    def standorte(self, routendatei):
        """Display all locations from a route file"""
        try:
            standortliste = dateifunktionen.get_standorte(routendatei=routendatei)
            print(f"DEBUG MapWidget: {len(standortliste)} Standorte für Route gefunden")
            
            for i, dummy in enumerate(standortliste):
                coords, name, time = standortliste[i]
                lat, lon = dateifunktionen.parse_coord_string_to_floats(coords)
                if lat is not None and lon is not None:
                    marker = self.map_widget.set_marker(lat, lon, text=name if name else "Unbenannt")
                    
                    if name: # Standort ist schon benannt
                        marker.marker_color_circle = "brown"
                    else: # Neuer Standort
                        marker.marker_color_circle = "red"
                        
                    self.markers.append(marker)
                    print(f"DEBUG MapWidget: Marker hinzugefügt: {name if name else 'Unbenannt'} bei ({lat:.6f}, {lon:.6f})")
        except Exception as e:
            print(f"DEBUG MapWidget: Fehler beim Anzeigen der Standorte: {e}")

    def set_position(self, lat, lon, zoom=None):
        """Set map position"""
        self.map_widget.set_position(lat, lon)
        if zoom:
            self.map_widget.set_zoom(zoom)
