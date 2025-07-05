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

    def place(self, x=0, y=0):
        """Place the map widget at specified coordinates"""
        self.map_widget.place(x=x, y=y)

    def pack(self, **kwargs):
        """Pack the map widget"""
        self.map_widget.pack(**kwargs)

    def grid(self, **kwargs):
        """Grid the map widget"""
        self.map_widget.grid(**kwargs)

    def clear_map(self):
        """Clear all markers and paths from the map"""
        # Clear markers
        for marker in self.markers:
            marker.delete()
        self.markers.clear()
        
        # Clear path
        if self.current_path:
            self.map_widget.delete_path(self.current_path)
            self.current_path = None

    def route(self, routendatei):
        """Zeigt die Route einer Routendatei samt all ihrer Standorte an. Bei Live Tracking wiederholt aufrufen zum aktualisieren."""
        try:
            self.clear_map()
            
            self.route_points = dateifunktionen.routendatei_zu_liste(routendatei)
            if self.route_points:
                self.current_path = self.map_widget.set_path(self.route_points)
                self.standorte(routendatei)
                
                if len(self.route_points) > 1:
                    deg_x, deg_y = self.route_points[len(self.route_points)-1]
                    self.map_widget.set_position(deg_x, deg_y)
        except Exception as e:
            print(f"Error displaying route: {e}")

    def standort(self, standortdatei):
        """Zeigt einen einzelnen Standort auf der Karte (für Standortmenü)"""
        try:
            self.clear_map()
            
            data = dateifunktionen.parse_standort_file(standortdatei)
            lat, lon = dateifunktionen.parse_coord_string_to_floats(data["location"])
            marker = self.map_widget.set_marker(lat, lon)
            
            if data["custom_name"] == data["location"]: # Standort ist noch nicht benannt = Rot
                marker.marker_color_circle = "red"
            else: # Standort ist schon benannt = Braun
                marker.marker_color_circle = "brown"
                
            self.markers.append(marker)
            self.map_widget.set_position(lat, lon)
        except Exception as e:
            print(f"Error displaying location: {e}")

    def standorte(self, routendatei):
        """Display all locations from a route file"""
        try:
            standortliste = dateifunktionen.get_standorte(routendatei=routendatei)
            for i, dummy in enumerate(standortliste):
                coords, name, time = standortliste[i]
                lat, lon = dateifunktionen.parse_coord_string_to_floats(coords)
                marker = self.map_widget.set_marker(lat, lon, text=name)
                
                if name: # Standort ist schon benannt
                    marker.marker_color_circle = "brown"
                else: # Neuer Standort
                    marker.marker_color_circle = "red"
                    
                self.markers.append(marker)
        except Exception as e:
            print(f"Error displaying locations: {e}")

    def set_position(self, lat, lon, zoom=None):
        """Set map position"""
        self.map_widget.set_position(lat, lon)
        if zoom:
            self.map_widget.set_zoom(zoom)

    def set_zoom(self, zoom):
        """Set map zoom level"""
        self.map_widget.set_zoom(zoom)
