#!/usr/bin/env python3
"""
Erstellt Test-Routen für verschiedene Tage zur Demonstration der chronologischen Sortierung
"""

import dateifunktionen
import os
from datetime import datetime, timedelta

def create_test_routes_for_multiple_days():
    """Erstellt Test-Routen für die letzten 5 Tage"""
    
    base_coordinates = [
        ("50.7421 7.0660", "08:00:00"),
        ("50.7422 7.0661", "08:01:00"),
        ("50.7423 7.0662", "08:02:00")
    ]
    
    today = datetime.now().date()
    
    print("Erstelle Test-Routen für verschiedene Tage...\n")
    
    for i in range(5):  # Letzten 5 Tage
        test_date = today - timedelta(days=i)
        folder_name = test_date.strftime("%Y-%m-%d")
        
        print(f"📅 Erstelle Routen für {folder_name}:")
        
        # Erstelle 2-3 Routen pro Tag
        routes_per_day = 2 if i < 2 else 3  # Heute und gestern 2 Routen, sonst 3
        
        for route_num in range(routes_per_day):
            hour = 8 + route_num * 4  # 8:00, 12:00, 16:00
            filename = f"test-route-{hour:02d}-00-00.json"
            
            print(f"  📄 {filename}")
            
            try:
                for j, (coords, time_part) in enumerate(base_coordinates):
                    # Variiere die Koordinaten leicht für verschiedene Routen
                    lat, lon = map(float, coords.split())
                    lat += i * 0.001 + route_num * 0.0005  # Kleine Variation
                    lon += i * 0.001 + route_num * 0.0005
                    
                    varied_coords = f"{lat:.6f} {lon:.6f}"
                    
                    # Erstelle Zeitstempel
                    hour_with_minutes = hour + (j * 1) // 60
                    minutes = (j * 1) % 60
                    timestamp = f"{test_date} {hour_with_minutes:02d}:{minutes:02d}:{j:02d}+00:00"
                    
                    dateifunktionen.gps_json_write(
                        varied_coords, 
                        timestamp, 
                        folder=folder_name, 
                        filename=filename
                    )
                    
            except Exception as e:
                print(f"    ❌ Fehler: {e}")
        
        print()

def main():
    print("=== ERSTELLE TEST-ROUTEN FÜR VERSCHIEDENE TAGE ===\n")
    
    # Erstelle Test-Routen
    create_test_routes_for_multiple_days()
    
    print("="*60 + "\n")
    
    # Zeige das Ergebnis
    print("ERGEBNIS - CHRONOLOGISCHE ROUTENLISTE:")
    print("-" * 40)
    
    alle_routen = dateifunktionen.get_all_routes_sorted()
    
    if alle_routen:
        current_date = None
        for i, route_info in enumerate(alle_routen, 1):
            if route_info['folder_date'] != current_date:
                current_date = route_info['folder_date']
                print(f"\n📅 {current_date}:")
            
            start_time = route_info['start_time'][:16] if route_info['start_time'] != 'Unbekannt' else 'Unbekannt'
            print(f"  {i:2d}. {route_info['file_name']} ({start_time}) - {route_info['num_points']} Punkte")
    else:
        print("Keine Routen gefunden.")

if __name__ == "__main__":
    main()
