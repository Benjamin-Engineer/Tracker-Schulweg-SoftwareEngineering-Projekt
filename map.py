import tkinter as tk  
import tkintermapview  
import os
import osmnx as ox  
import networkx as nx 
import dateifunktionen


class GPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPS Tracker")

        # Kartenwidget
        self.map_widget = tkintermapview.TkinterMapView(root, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(50.7374, 7.0982)  # (Bonn)
        self.map_widget.set_zoom(15)

    def route(self, routendatei):
        """Zeigt die Route einer Routendatei samt all ihrer Standorte an. Bei Live Tracking wiederholt aufrufen zum aktualisieren."""
        self.route_points = dateifunktionen.routendatei_zu_liste(routendatei)
        self.map_widget.set_path(self.route_points)
        self.standorte(routendatei)
        if len(self.route_points) > 1:
            deg_x, deg_y = self.route_points[len(self.route_points)-1]
            self.map_widget.set_position(deg_x,deg_y)

    def standort(self, standortdatei):
        """Zeigt einen einzelnen Standort auf der Karte (für Standortmenü)"""
        data = dateifunktionen.parse_standort_file(standortdatei)
        lat, lon = dateifunktionen.parse_coord_string_to_floats(data["location"])
        marker = self.map_widget.set_marker(lat, lon)
        if data["custom_name"] == data["location"]: # Standort ist noch nicht benannt = Rot
                marker.marker_color_circle = "red"
        else: # Standort ist schon benannt = Braun
                marker.marker_color_circle = "brown"


    def standorte(self, routendatei):
        standortliste = dateifunktionen.get_standorte(routendatei=routendatei)
        for i, dummy in enumerate(standortliste):
            coords, name, time = standortliste[i]
            lat, lon = dateifunktionen.parse_coord_string_to_floats(coords)
            marker = self.map_widget.set_marker(lat, lon, text=name)
            if name: # Standort ist schon benannt
                marker.marker_color_circle = "brown"
            else: # Neuer Standort
                marker.marker_color_circle = "red"


# Test

datei = "2025-07-01/2025-07-01 19-57-44-297620.json"


if __name__ == "__main__":

    root = tk.Tk()
    app = GPSApp(root) # Dateipfade der Routendatei
    root.mainloop()
    #app.standort("Standorte/50.000000 7.000000.txt")
    app.route("2025-07-01/2025-07-01 19-57-44-297620.json")