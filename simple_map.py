import tkinter as tk  # GUI-Toolkit
import tkintermapview  # Karten-Widget für Tkinter
import random  # Für simulierte GPS-Daten
import time  # Für Zeitmessung bei Aufenthalten
import math  # Für Distanzberechnung

class GPSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPS Tracker")

        # Erstelle das Karten-Widget mit festgelegter Größe und ohne abgerundete Ecken
        self.map_widget = tkintermapview.TkinterMapView(root, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(50.7374, 7.0982)  # Setze Startposition auf Bonn
        self.map_widget.set_zoom(15)  # Setze Zoomstufe

        # Erstelle Button-Leiste für Start/Stop
        self.button_frame = tk.Frame(root)
        self.button_frame.pack()
        self.start_button = tk.Button(self.button_frame, text="Start Route", command=self.start_route)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = tk.Button(self.button_frame, text="Stop Route", command=self.stop_route)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Variablen für das Tracking und die Routenspeicherung
        self.tracking = False  # Gibt an, ob Tracking aktiv ist
        self.route_points = []  # Liste der GPS-Punkte der Route
        self.last_stationary_point = None  # Letzter Punkt für Aufenthaltsprüfung
        self.stationary_start_time = None  # Startzeit des Aufenthalts
        self.stationary_marked = False  # Ob Aufenthalt bereits markiert wurde

        # Schrittzähler für die GPS-Simulation
        self.simulation_step = 0
        self.simulation_timer()  # Starte die Simulation

    def start_route(self):
        """Starte das Tracking und setze alle Variablen zurück."""
        self.tracking = True
        self.route_points = []
        self.stationary_marked = False
        self.last_stationary_point = None
        self.stationary_start_time = None
        self.simulation_step = 0
        self.map_widget.delete_all_path()  # Lösche vorherige Routen von der Karte
        print("Route gestartet")

    def stop_route(self):
        """Beende das Tracking."""
        self.tracking = False
        print("Route gestoppt")

    def simulation_timer(self):
        """Timer, der alle 5 Sekunden neue GPS-Daten simuliert."""
        if self.tracking:
            self.simulate_gps_data()
        self.root.after(5000, self.simulation_timer)  # Wiederhole alle 5 Sekunden

    def simulate_gps_data(self):
        """
        Simuliere GPS-Daten:
        - Zuerst Bewegung (3 Schritte)
        - Dann Aufenthalt (3 Schritte)
        - Dann wieder Bewegung
        """
        if self.simulation_step < 3:
            # Bewegung simulieren
            if not self.route_points:
                lat, lon = 50.7374, 7.0982  # Startkoordinaten
            else:
                lat, lon = self.route_points[-1]
                lat += random.uniform(-0.0002, 0.0002)
                lon += random.uniform(-0.0002, 0.0002)
            self.route_points.append((lat, lon))

        elif 3 <= self.simulation_step < 6:
            # Aufenthalt simulieren (gleicher Punkt)
            lat, lon = self.route_points[-1]
            self.route_points.append((lat, lon))

        else:
            # Weitere Bewegung simulieren
            lat, lon = self.route_points[-1]
            lat += random.uniform(-0.0002, 0.0002)
            lon += random.uniform(-0.0002, 0.0002)
            self.route_points.append((lat, lon))

        # Zeichne die Route auf der Karte, wenn mehr als ein Punkt vorhanden ist
        if len(self.route_points) > 1:
            self.map_widget.set_path(self.route_points)

        self.check_stationary(lat, lon)  # Prüfe auf längeren Aufenthalt
        print(f"Schritt {self.simulation_step}: Punkt: {lat}, {lon}")
        self.simulation_step += 1

    def check_stationary(self, lat, lon):
        """
        Prüfe, ob der Nutzer länger an einem Ort verweilt.
        Wenn ja, markiere diesen Punkt auf der Karte.
        """
        if self.stationary_marked:
            return  # Bereits markiert

        if self.last_stationary_point is None:
            # Erster Punkt für Aufenthaltsprüfung
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
        R = 6371000  # Erdradius in Metern
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

if __name__ == "__main__":
    # Starte die Anwendung
    root = tk.Tk()
    app = GPSApp(root)
    root.mainloop()