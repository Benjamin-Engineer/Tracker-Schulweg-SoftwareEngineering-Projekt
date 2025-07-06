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

class gesperrtpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
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

        self.create_button("entsperren.png", 1280.0, 0.0, 
                          lambda: self.handle_unlock(), 640.0, 1080.0)

        self.create_button("ausschalten.png", 51.0, 929.0,
                          lambda: system_shutdown(), 100.0, 100.0) #ausschaltenfunktion einfügen
        
        # Initialize and place the map widget on the left side of the lock screen
        self.map_widget = MapWidget(self, width=1280, height=1080)
        self.map_widget.place(x=0, y=0)

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

    def handle_unlock(self):
        from start import startpage
        print("Unlock attempt")
        #einfügen des öffnen eines entry feldes
        #import pin.py -check pin if else für pin abfrage
        self.controller.show_frame(startpage)

    def update_map_with_route(self, route_file=None):
        """
        Update the map with current route data
        Call this method to show current tracking route on lock screen
        """
        if route_file and self.map_widget:
            try:
                self.map_widget.route(route_file)
                print(f"Lock screen map updated with route: {route_file}")
            except Exception as e:
                print(f"Error updating lock screen map: {e}")

    def on_show(self):
        """
        Called when lock screen is shown
        Shows current simulation route ONLY if simulation is running
        """
        # Check if GPS simulation is running and show live data
        try:
            from tracking import trackingpage
            if hasattr(self.controller, 'frames'):
                tracking_frame = self.controller.frames.get(trackingpage)
                if tracking_frame and tracking_frame.tracking and tracking_frame.route_points:
                    # Show live simulation route
                    if len(tracking_frame.route_points) > 1:
                        self.map_widget.map_widget.set_path(tracking_frame.route_points, color="#0000FF", width=6)
                    
                    # Center camera on the latest GPS point immediately
                    if tracking_frame.route_points:
                        latest_lat, latest_lon = tracking_frame.route_points[-1]
                        self.map_widget.map_widget.set_position(latest_lat, latest_lon)
                        print(f"Lock screen camera initially centered on: {latest_lat:.6f}, {latest_lon:.6f}")
                    
                    print("Lock screen showing live simulation data")
                    # Schedule regular updates while lock screen is active
                    self.schedule_map_update()
                    return
        except Exception as e:
            print(f"Error showing live simulation data: {e}")
        
        # If no simulation is running, clear any existing routes and show default map
        try:
            # Clear any existing paths on the map
            self.map_widget.map_widget.delete_all_path()
            print("No active simulation - showing default map view without routes")
        except Exception as e:
            print(f"Error clearing map paths: {e}")
            # Map will show default position (Bonn)
            
    def schedule_map_update(self):
        """Schedule regular map updates while lock screen is active"""
        if hasattr(self, 'controller') and hasattr(self.controller, 'frames'):
            try:
                from tracking import trackingpage
                tracking_frame = self.controller.frames.get(trackingpage)
                if tracking_frame and tracking_frame.tracking and tracking_frame.route_points:
                    # Update map with current route
                    if len(tracking_frame.route_points) > 1:
                        self.map_widget.map_widget.set_path(tracking_frame.route_points, color="#0000FF", width=6)
                    
                    # Center camera on the latest GPS point (like in tracking page)
                    if tracking_frame.route_points:
                        latest_lat, latest_lon = tracking_frame.route_points[-1]
                        self.map_widget.map_widget.set_position(latest_lat, latest_lon)
                        print(f"Lock screen camera centered on: {latest_lat:.6f}, {latest_lon:.6f}")
                    
                    # Schedule next update in 5 seconds if still tracking
                    self.after(5000, self.schedule_map_update)
            except Exception as e:
                print(f"Error updating lock screen map: {e}")