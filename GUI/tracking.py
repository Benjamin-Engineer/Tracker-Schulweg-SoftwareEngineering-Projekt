from pathlib import Path

import tkinter as tk

# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image

import sys
import os
import random
import time
import math
import json
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shutdown import system_shutdown
from map_widget import MapWidget
import dateifunktionen

# Try to import osmnx and networkx for realistic routes
try:
    import osmnx as ox
    import networkx as nx
    HAS_OSMNX = True
except ImportError:
    HAS_OSMNX = False
    print("Warning: osmnx not available, using simple route simulation")

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/GUI/assets")


def relative_to_assets(path: str) -> Path:
    ASSETS_PATH = Path(__file__).parent / "assets"
    return ASSETS_PATH / Path(path)

class trackingpage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        from einstellungen import einstellungenpage
        from standorte_menü import standorte_menüpage
        from routen_menü import routen_menüpage
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

        self.create_button("export.png", 1280, 0, lambda: print("Export clicked"), 640, 216)
        self.create_button("einstellungen.png", 1280, 216, lambda: controller.show_frame(einstellungenpage), 640, 216)
        self.create_button("standorte.png", 1280, 432, lambda: controller.show_frame(standorte_menüpage), 640, 216)
        self.create_button("routen.png", 1280, 648, lambda: controller.show_frame(routen_menüpage), 640, 216)
        self.create_button("stop.png", 1280, 864, lambda: self.stop_tracking_and_return(), 640, 216)

        # Initialize and place the map widget - this will show live tracking
        self.map_widget = MapWidget(self, width=1280, height=1080)
        self.map_widget.place(x=0, y=0)
        
        # Shutdown button NACH dem MapWidget erstellen, damit er darüber liegt
        self.create_button("ausschalten.png", 51, 929, lambda: system_shutdown(), 100.0, 100.0)
        
        # GPS Simulation variables
        self.tracking = False
        self.route_points = []
        self.last_stationary_point = None
        self.stationary_start_time = None
        self.stationary_marked = False
        self.simulation_step = 0
        self.stationary_simulation_point = None
        self.stationary_simulation_count = 0
        self.route_gps_points = []
        self.current_route_file = None
        
        # Standorte-Speicherung für Route
        self.detected_standorte = []  # Liste der erkannten Standorte [(lat, lon, timestamp)]
        
        # Kamera-Verfolgung aktiviert (automatisch dem GPS-Punkt folgen)
        self.camera_follow_enabled = True
        
        # Start simulation timer
        self.simulation_timer_active = False

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

    def update_live_tracking(self, route_file=None):
        """
        Update the map with live tracking data
        Call this method periodically during active tracking
        """
        if route_file and self.map_widget:
            self.map_widget.route(route_file)

    def start_gps_simulation(self):
        """Start GPS simulation when called from start button"""
        print("Starting GPS simulation...")
        
        # First, reset all simulation state to ensure clean start
        self.reset_simulation_state()
        
        # Now set up for new simulation
        self.tracking = True
        self.route_points = []
        self.stationary_marked = False
        self.last_stationary_point = None
        self.stationary_start_time = None
        self.simulation_step = 0
        self.stationary_simulation_point = None
        self.stationary_simulation_count = 0
        
        # EXPLICITLY clear previous routes from map
        print("Clearing map for new simulation...")
        if self.map_widget:
            self.map_widget.clear_map()
            # Also force delete all paths as backup
            try:
                self.map_widget.map_widget.delete_all_path()
                self.map_widget.map_widget.delete_all_marker()
            except Exception as e:
                print(f"Additional cleanup attempt: {e}")
        
        # Create new route file for this session
        self.create_route_file()
        
        # Generate new realistic route
        self.generate_realistic_route()
        
        # Start simulation timer
        if not self.simulation_timer_active:
            self.simulation_timer_active = True
            self.controller.schedule_simulation_timer(self.simulation_timer)
            
        print(f"New GPS simulation started. Route file: {self.current_route_file}")

    def stop_gps_simulation(self):
        """Stop GPS simulation"""
        print("Stopping GPS simulation...")
        self.tracking = False
        self.simulation_timer_active = False
        
        # Save final route data if we have points
        if self.current_route_file and self.route_points:
            self.save_route_points()
            print(f"Route saved with {len(self.route_points)} points to: {self.current_route_file}")
            
            # Notify route menu to refresh the list
            self.notify_route_menu_refresh()
        else:
            print("No route data to save")

    def notify_route_menu_refresh(self):
        """Notify the route menu to refresh its route list"""
        try:
            from routen_menü import routen_menüpage
            if hasattr(self.controller, 'frames'):
                route_menu_frame = self.controller.frames.get(routen_menüpage)
                if route_menu_frame and hasattr(route_menu_frame, 'load_routes'):
                    # Schedule refresh for after potential frame switch
                    self.after(100, route_menu_frame.load_routes)
                    print("Route menu will be refreshed")
        except Exception as e:
            print(f"Error notifying route menu: {e}")

    def notify_standorte_menu_refresh(self):
        """Benachrichtige das Standorte-Menü über neue Standorte"""
        try:
            from standorte_menü import standorte_menüpage
            if hasattr(self.controller, 'frames'):
                standorte_menu_frame = self.controller.frames.get(standorte_menüpage)
                if standorte_menu_frame and hasattr(standorte_menu_frame, 'refresh_standorte'):
                    # Schedule refresh for after potential frame switch
                    self.after(100, standorte_menu_frame.refresh_standorte)
                    print("Standorte-Menü wird aktualisiert")
        except Exception as e:
            print(f"Fehler beim Benachrichtigen des Standorte-Menüs: {e}")

    def reset_simulation_state(self):
        """Reset all simulation variables for a fresh start"""
        print("Resetting simulation state...")
        self.tracking = False
        self.route_points = []
        self.last_stationary_point = None
        self.stationary_start_time = None
        self.stationary_marked = False
        self.simulation_step = 0
        self.stationary_simulation_point = None
        self.stationary_simulation_count = 0
        self.route_gps_points = []  # This will force generation of a new route
        self.current_route_file = None
        self.simulation_timer_active = False
        
        # Reset Standorte-Liste für neue Simulation
        self.detected_standorte = []
        
        # Kamera-Verfolgung für neue Simulation aktivieren
        self.camera_follow_enabled = True
        
        # Clear the map thoroughly
        if self.map_widget:
            print("Clearing map in reset_simulation_state...")
            self.map_widget.clear_map()
            # Additional cleanup to be absolutely sure
            try:
                self.map_widget.map_widget.delete_all_path()
                self.map_widget.map_widget.delete_all_marker()
                print("Map cleared successfully")
            except Exception as e:
                print(f"Map clearing warning: {e}")
        
        print("Simulation state reset for new route")

    def create_route_file(self):
        """Create a unique route file for today's tracking session"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Create directory if it doesn't exist
            route_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', today))
            os.makedirs(route_dir, exist_ok=True)
            
            # Generate unique filename with current timestamp
            timestamp = datetime.now()
            time_str = timestamp.strftime("%H-%M-%S-%f")  # Include microseconds for uniqueness
            
            # Create route file path
            self.current_route_file = os.path.join(route_dir, f"{time_str}.json")
            
            # Ensure filename is unique (in case of rapid starts)
            counter = 1
            base_file = self.current_route_file
            while os.path.exists(self.current_route_file):
                name_part = base_file.replace('.json', f'_{counter}.json')
                self.current_route_file = name_part
                counter += 1
            
            # Initialize empty route file
            route_metadata = {
                "start_time": timestamp.isoformat(),
                "end_time": None,
                "points_count": 0,
                "route_data": []
            }
            
            with open(self.current_route_file, 'w') as f:
                json.dump(route_metadata, f, indent=2)
                
            print(f"Created new route file: {self.current_route_file}")
            
        except Exception as e:
            print(f"Error creating route file: {e}")
            self.current_route_file = None

    def save_route_points(self):
        """Save current route points to the route file with metadata"""
        if not self.current_route_file or not self.route_points:
            return
            
        try:
            # Prepare route data with timestamps
            route_data = []
            start_time = datetime.now().timestamp() - (len(self.route_points) * 5)  # 5 seconds between points
            
            for i, (lat, lon) in enumerate(self.route_points):
                point_time = start_time + (i * 5)  # 5 seconds between points
                route_data.append({
                    "latitude": lat,
                    "longitude": lon,
                    "timestamp": point_time,
                    "step": i + 1
                })
            
            # Create complete route metadata
            end_time = datetime.now()
            route_metadata = {
                "start_time": datetime.fromtimestamp(start_time).isoformat(),
                "end_time": end_time.isoformat(),
                "points_count": len(self.route_points),
                "duration_seconds": len(self.route_points) * 5,
                "simulation_type": "GPS_Simulation",
                "has_stationary_points": self.stationary_marked,
                "detected_standorte": self.detected_standorte,  # **STANDORTE HINZUFÜGEN**
                "route_data": route_data
            }
            
            # Save to file
            with open(self.current_route_file, 'w') as f:
                json.dump(route_metadata, f, indent=2)
                
            print(f"Route saved successfully:")
            print(f"  - File: {self.current_route_file}")
            print(f"  - Points: {len(route_data)}")
            print(f"  - Duration: {route_metadata['duration_seconds']} seconds")
            print(f"  - Stationary points: {self.stationary_marked}")
            print(f"  - Detected standorte: {len(self.detected_standorte)}")
            
        except Exception as e:
            print(f"Error saving route points: {e}")
            import traceback
            traceback.print_exc()

    def generate_realistic_route(self):
        """Generate realistic route using osmnx or fallback to simple route"""
        print("Generating completely NEW route...")
        if HAS_OSMNX:
            self.generate_osmnx_route()
        else:
            self.generate_simple_route()
        print(f"NEW route generated with {len(self.route_gps_points)} points")

    def generate_osmnx_route(self):
        """Generate realistic route using OpenStreetMap data"""
        try:
            import random
            center_point = (50.7374, 7.0982)  # Bonn
            G = ox.graph_from_point(center_point, dist=1500, network_type='walk')
            nodes = list(G.nodes)
            
            # Choose random start and end points for variety
            start_node = random.choice(nodes)
            end_node = random.choice(nodes)
            
            # Ensure start and end are different
            while start_node == end_node:
                end_node = random.choice(nodes)
            
            route = nx.shortest_path(G, start_node, end_node, weight='length')
            gps_points = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]
            
            # Interpolate points every 15 meters
            interpolated_points = []
            for i in range(len(gps_points) - 1):
                lat1, lon1 = gps_points[i]
                lat2, lon2 = gps_points[i+1]
                dist = self.haversine_distance(lat1, lon1, lat2, lon2)
                steps = max(1, int(dist // 15))  # ca. alle 15 Meter ein Punkt
                for s in range(steps):
                    frac = s / steps
                    lat = lat1 + (lat2 - lat1) * frac
                    lon = lon1 + (lon2 - lon1) * frac
                    interpolated_points.append((lat, lon))
            interpolated_points.append(gps_points[-1])
            
            self.route_gps_points = interpolated_points
            print(f"Generated NEW realistic route with {len(self.route_gps_points)} points (osmnx)")
            print(f"Generated realistic route with {len(self.route_gps_points)} points")
            
        except Exception as e:
            print(f"Error generating osmnx route: {e}")
            self.generate_simple_route()

    def generate_simple_route(self):
        """Generate simple circular route around Bonn as fallback"""
        import random
        import math
        
        center_lat, center_lon = 50.7374, 7.0982
        
        # Add some randomness to make each route different
        radius = 0.005 + random.random() * 0.01  # Random radius between 0.005 and 0.015
        num_points = 30 + random.randint(0, 40)  # Random number of points between 30-70
        start_angle = random.random() * 2 * math.pi  # Random starting angle
        direction = random.choice([1, -1])  # Random direction (clockwise or counterclockwise)
        
        points = []
        for i in range(num_points):
            angle = start_angle + direction * 2 * math.pi * i / num_points
            # Add small random variations to make route more natural
            lat_variation = (random.random() - 0.5) * 0.001
            lon_variation = (random.random() - 0.5) * 0.001
            
            lat = center_lat + radius * math.cos(angle) + lat_variation
            lon = center_lon + radius * math.sin(angle) + lon_variation
            points.append((lat, lon))
        
        self.route_gps_points = points
        print(f"Generated NEW simple route with {len(self.route_gps_points)} points (fallback)")

    def simulation_timer(self):
        """Timer that generates new GPS data every 5 seconds"""
        if self.tracking and self.simulation_timer_active:
            self.simulate_gps_data()
            # Schedule next simulation step via main controller to keep running during lock screen
            self.controller.schedule_simulation_timer(self.simulation_timer)

    def simulate_gps_data(self):
        """Simulate GPS movement along the generated route"""
        if not self.route_gps_points or self.simulation_step >= len(self.route_gps_points):
            print("Route completed - stopping simulation")
            self.stop_gps_simulation()
            return

        # Determine if we should simulate a stationary point
        if (self.stationary_simulation_point is None and 
            len(self.route_gps_points) > 10 and 
            self.simulation_step > 5):
            middle_start = len(self.route_gps_points) // 3
            middle_end = 2 * len(self.route_gps_points) // 3
            self.stationary_simulation_point = random.randint(middle_start, middle_end)
            print(f"Stationary point planned at step {self.stationary_simulation_point}")

        # Check if we're at the stationary point
        if (self.stationary_simulation_point is not None and 
            self.simulation_step == self.stationary_simulation_point and 
            self.stationary_simulation_count < 15):  # 75 seconds stationary (15 * 5 seconds)
            
            # PAUSIERE HIER: Bleibe exakt an diesem Punkt stehen
            lat, lon = self.route_gps_points[self.stationary_simulation_point]
            # Minimale Variation (1-2 Meter) um GPS-Ungenauigkeit zu simulieren
            lat += random.uniform(-0.00001, 0.00001)  
            lon += random.uniform(-0.00001, 0.00001)
            self.stationary_simulation_count += 1
            print(f"🛑 SIMULATION PAUSIERT - Stationary simulation: {self.stationary_simulation_count}/15 (an Punkt {self.stationary_simulation_point})")
            
            # WICHTIG: simulation_step wird NICHT erhöht, bis die stationäre Zeit vorbei ist!
            if self.stationary_simulation_count >= 15:
                print("✅ Stationary simulation beendet - Bewegung wird fortgesetzt")
                self.simulation_step += 1  # Erst JETZT zur nächsten Position
        else:
            # Normal movement along route
            lat, lon = self.route_gps_points[self.simulation_step]
            self.simulation_step += 1
            print(f"🚶 Normale Bewegung: Schritt {self.simulation_step}/{len(self.route_gps_points)}")

        # Add point to route
        self.route_points.append((lat, lon))
        
        # Update map with new path
        if len(self.route_points) > 1:
            self.map_widget.map_widget.set_path(self.route_points, color="#0000FF", width=6)
        
        # **KAMERA-VERFOLGUNG**: Automatisch dem aktuellen GPS-Punkt folgen
        if self.camera_follow_enabled:
            self.map_widget.map_widget.set_position(lat, lon)
            print(f"Kamera folgt GPS-Position: {lat:.6f}, {lon:.6f}")
        
        # Check for stationary behavior
        self.check_stationary(lat, lon)
        
        # Save progress periodically
        if len(self.route_points) % 10 == 0:  # Save every 10 points
            self.save_route_points()
        
        print(f"Step {len(self.route_points)}: {lat:.6f}, {lon:.6f}")

    def check_stationary(self, lat, lon):
        """Check if user is stationary and mark on map"""
        if self.stationary_marked:
            return

        if self.last_stationary_point is None:
            self.last_stationary_point = (lat, lon)
            self.stationary_start_time = time.time()
        else:
            dist = self.haversine_distance(lat, lon, *self.last_stationary_point)
            if dist < 20:  # Less than 20 meters movement
                duration = time.time() - self.stationary_start_time
                if duration >= 60:  # Stationary for more than 1 minute
                    marker = self.map_widget.map_widget.set_marker(lat, lon, text="Längerer Aufenthalt")
                    if hasattr(marker, 'marker_color_circle'):
                        marker.marker_color_circle = "red"
                    self.stationary_marked = True
                    
                    # **STANDORT SPEICHERN**: Erkannten Standort zur Liste hinzufügen
                    standort_info = {
                        "latitude": lat,
                        "longitude": lon,
                        "timestamp": datetime.now().isoformat(),
                        "duration_seconds": duration,
                        "description": "Längerer Aufenthalt (Simulation)"
                    }
                    self.detected_standorte.append(standort_info)
                    
                    # **STANDORT-DATEI ERSTELLEN**: Für bessere Integration mit bestehendem System
                    try:
                        coordinates_str = f"{lat:.6f} {lon:.6f}"
                        timestamp_str = standort_info["timestamp"]
                        dateifunktionen.erstelle_standortdatei(coordinates_str, timestamp_str)
                        print(f"Standort-Datei erstellt: {coordinates_str}")
                        
                        # Benachrichtige das Standorte-Menü über den neuen Standort
                        self.notify_standorte_menu_refresh()
                        
                    except Exception as e:
                        print(f"Fehler beim Erstellen der Standort-Datei: {e}")
                    
                    print(f"Standort gespeichert: {lat:.6f}, {lon:.6f} (Dauer: {duration:.1f}s)")
                    
                    print("Stationary location detected and marked")
            else:
                # Movement detected, reset stationary check
                self.last_stationary_point = (lat, lon)
                self.stationary_start_time = time.time()

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two GPS coordinates in meters"""
        R = 6371000  # Earth radius in meters
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def stop_tracking_and_return(self):
        """Stop tracking simulation and return to start page"""
        from start import startpage
        
        if self.tracking and self.route_points:
            # Save the route
            self.stop_gps_simulation()
            print(f"✓ Route mit {len(self.route_points)} Punkten gespeichert!")
            print("  Die Route ist jetzt unter 'Routen' verfügbar.")
        else:
            # Just stop without saving if no data
            self.stop_gps_simulation()
            print("GPS-Simulation gestoppt (keine Daten zum Speichern)")
        
        # Return to start page
        self.controller.show_frame(startpage)