import tkinter as tk  
import tkintermapview  
import random  
import time  
import math  
import osmnx as ox  
import networkx as nx 
import dateifunktionen

def split_coordinates_string_to_floats(coord_tpl):
    """
    Splits a coordinate string "lat lon" into two float values (latitude, longitude).
    Returns (latitude, longitude) or (None, None) if parsing fails.
    """
    try:
        lat_flt, lon_flt = coord_tpl.split()
        lat = float(lat_flt)
        lon = float(lon_flt)
        return lat, lon
    except ValueError:
        return None, None

def parse_coordinates(coords):
    """
    Parses coordinates from a string "lat lon" or a tuple/list (lat, lon).
    Returns (latitude, longitude) as floats, or (None, None) if parsing fails.
    """
    if isinstance(coords, str):
        try:
            lat_str, lon_str = coords.split()
            lat = float(lat_str)
            lon = float(lon_str)
            return lat, lon
        except ValueError:
            return None, None
    elif isinstance(coords, (tuple, list)) and len(coords) == 2:
        try:
            lat = float(coords[0])
            lon = float(coords[1])
            return lat, lon
        except (ValueError, TypeError):
            return None, None
    return None, None

class GPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPS Tracker")

        # Kartenwidget
        self.map_widget = tkintermapview.TkinterMapView(root, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(50.7374, 7.0982)  # (Bonn)
        self.map_widget.set_zoom(15)  

        self.tracking = False
        self.route_points = [] 
        self.last_stationary_point = None
        self.stationary_start_time = None 
        self.stationary_marked = False

        # GPs-Simulation (Schrittzähler )
        self.simulation_step = 0
        self.simulation_timer()  # Starte die Simulation

        self.standorte()

    def start_route(self):
        """Starte das Tracking und setze alle Variablen zurück."""
        self.tracking = True
        self.route_points = []
        self.stationary_marked = False
        self.last_stationary_point = None
        self.stationary_start_time = None
        self.simulation_step = 0
        self.map_widget.delete_all_path() 
        print("Route gestartet")
        self.generate_realistic_route() 
    def generate_realistic_route(self):
        """
        Berechnet eine realistische Route auf Straßen in Bonn mit osmnx.
        Interpoliert die Route so, dass die Schritte ca. 10-20 Meter auseinander liegen.
        """
        center_point = (50.7374, 7.0982)
        G = ox.graph_from_point(center_point, dist=1500, network_type='walk')
        nodes = list(G.nodes)
        start_node = ox.nearest_nodes(G, center_point[1], center_point[0])
        end_node = random.choice(nodes)
        try:
            route = nx.shortest_path(G, start_node, end_node, weight='length')
        except Exception as e:
            print(f"Routing-Fehler: {e}")
            return
        gps_points = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]
       
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
        self.simulation_step = 0
        print(f"Route mit {len(self.route_gps_points)} interpolierten Punkten generiert.")

    def stop_route(self):
        """Beende das Tracking."""
        self.tracking = False
        print("Route gestoppt")

    def simulation_timer(self):
        """Timer, der alle 5 Sekunden neue GPS-Daten simuliert."""
        if self.tracking:
            self.simulate_gps_data()
        self.root.after(5000, self.simulation_timer)  # Wiederhole alle 5 Sekunden (3-5m/s)
        if len(self.route_points) > 1:
            self.map_widget.set_position(self.route_points[len(self.route_points)-1][0], self.route_points[len(self.route_points)-1][1])

    def standorte(self):
        standortliste = dateifunktionen.get_standorte()
        for i in standortliste:
            lat, lon = split_coordinates_string_to_floats(standortliste[i][0])
            marker = self.map_widget.set_marker(lat, lon, text=standortliste[i][1])
            if standortliste[i][1]:
                marker.canvas_item.config(font=("Arial", 14, "bold"), fill="brown")
            else:
                marker.canvas_item.config(font=("Arial", 14, "bold"), fill="red")


#standortliste[i][0][0], standortliste[i][0][1],

if __name__ == "__main__":
    
    root = tk.Tk()
    app = GPSApp(root)
    root.mainloop()

# TEST
#a = GPSApp(root)