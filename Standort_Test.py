import tkinter as tk  
import tkintermapview  
import random  
import time  
import math  
import osmnx as ox  
import networkx as nx  

class GPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPS Tracker")

        # Kartenwidget
        self.map_widget = tkintermapview.TkinterMapView(root, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(50.7374, 7.0982)  # (Bonn)
        self.map_widget.set_zoom(15)  #

        # Start/Stop Button
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()
        self.start_button = tk.Button(self.button_frame, text="Start Route", command=self.start_route)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = tk.Button(self.button_frame, text="Stop Route", command=self.stop_route)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Tracking/Speicherung der Routen
        self.tracking = False  
        self.route_points = []  
        self.last_stationary_point = None  
        self.stationary_start_time = None  
        self.stationary_marked = False  

        # GPs-Simulation (Schrittzähler )
        self.simulation_step = 0
        self.simulation_timer() 

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
        self.root.after(5000, self.simulation_timer)  # Wiederhole alle 5 Sekunden (3-5 m/s)

    def simulate_gps_data(self):
        """
        Simuliert die Bewegung entlang einer echten Route (Straßen/Wege).
        Ab Schritt 5 bleibt der Nutzer für 15 Schritte am gleichen Punkt stehen, um einen Aufenthalt zu simulieren.
        """
        if hasattr(self, 'route_gps_points') and self.simulation_step < len(self.route_gps_points):
            # Ab Schritt 5 bis Schritt 20 immer den gleichen Punkt verwenden (test)
            if 5 <= self.simulation_step < 20:
                lat, lon = self.route_gps_points[5]
            else:
                lat, lon = self.route_gps_points[self.simulation_step]
            self.route_points.append((lat, lon))
            
            if len(self.route_points) > 1:
                self.map_widget.set_path(self.route_points)
            self.check_stationary(lat, lon)  # Prüfe auf längeren Aufenthalt
            print(f"Schritt {self.simulation_step}: Punkt: {lat}, {lon}")
            self.simulation_step += 1
        else:
            print("Route beendet oder nicht generiert.")
            self.tracking = False

    def check_stationary(self, lat, lon):
        """
        Prüfe, ob der Nutzer länger an einem Ort verweilt.
        Wenn ja, markiere diesen Punkt auf der Karte.
        """
        if self.stationary_marked:
            return  

        if self.last_stationary_point is None:
            
            self.last_stationary_point = (lat, lon)
            self.stationary_start_time = time.time()
        else:
            dist = self.haversine_distance(lat, lon, *self.last_stationary_point)
            if dist < 20:  # Weniger als 20 Meter Bewegung
                duration = time.time() - self.stationary_start_time
                if duration >= 60:  # Aufenthalt länger als 1 Minute
                    marker = self.map_widget.set_marker(lat, lon, text="Längerer Aufenthalt")
                    marker.canvas_item.config(font=("Arial", 14, "bold"), fill="red")
                    self.stationary_marked = True
                    print("Längerer Aufenthalt erkannt und markiert.")
            else:
                # Bewegung erkannt, Aufenthaltsprüfung zurücksetzen
                self.last_stationary_point = (lat, lon)
                self.stationary_start_time = time.time()

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """
        Berechnet die Entfernung zwischen zwei GPS-Koordinaten in Metern.
        """
        R = 6371000 
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

if __name__ == "__main__":
    
    root = tk.Tk()
    app = GPSApp(root)
    root.mainloop()
