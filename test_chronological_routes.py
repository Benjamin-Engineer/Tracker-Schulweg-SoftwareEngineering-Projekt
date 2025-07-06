#!/usr/bin/env python3
"""
Test-Skript zur Demonstration der chronologischen Routen-Sortierung
"""

import datetime
import dateifunktionen
import os

def main():
    print("=== DEMONSTRATION DER CHRONOLOGISCHEN ROUTEN-SORTIERUNG ===\n")
    
    # 1. Zeige alle verfügbaren Datumsordner
    print("1. VERFÜGBARE DATUMSORDNER MIT ROUTEN:")
    print("-" * 50)
    datumsordner = dateifunktionen.get_all_route_folders()
    
    if datumsordner:
        print(f"Insgesamt {len(datumsordner)} Datumsordner gefunden:")
        for ordner_pfad, ordner_datum, ordner_name in datumsordner:
            try:
                json_dateien = [f for f in os.listdir(ordner_pfad) if f.endswith('.json')]
                print(f"  📁 {ordner_name} ({ordner_datum}) - {len(json_dateien)} Routen")
                
                # Zeige die ersten 3 Routen in diesem Ordner
                if json_dateien:
                    for i, json_datei in enumerate(sorted(json_dateien)[:3]):
                        print(f"     📄 {json_datei}")
                    if len(json_dateien) > 3:
                        print(f"     ... und {len(json_dateien) - 3} weitere")
            except Exception as e:
                print(f"  ❌ Fehler beim Lesen von {ordner_name}: {e}")
    else:
        print("❌ Keine Datumsordner mit Routen gefunden.")
    
    print("\n" + "="*70 + "\n")
    
    # 2. Zeige alle Routen chronologisch sortiert
    print("2. ALLE ROUTEN CHRONOLOGISCH SORTIERT (NEUESTE ZUERST):")
    print("-" * 50)
    alle_routen = dateifunktionen.get_all_routes_sorted()
    
    if alle_routen:
        print(f"Insgesamt {len(alle_routen)} Routen gefunden:\n")
        
        current_date = None
        for i, route_info in enumerate(alle_routen, 1):
            # Gruppiere nach Datum
            if route_info['folder_date'] != current_date:
                current_date = route_info['folder_date']
                print(f"\n📅 {current_date}:")
                print("   " + "-" * 40)
            
            # Zeige Route-Details
            start_time_short = route_info['start_time'][:19] if route_info['start_time'] != 'Unbekannt' else 'Unbekannt'
            print(f"   {i:2d}. {route_info['file_name']}")
            print(f"       ⏰ Start: {start_time_short}")
            print(f"       📍 Punkte: {route_info['num_points']}")
            print(f"       📂 Pfad: {route_info['file_path']}")
            
            if i >= 10:  # Limitiere die Ausgabe auf die ersten 10 Routen
                remaining = len(alle_routen) - 10
                if remaining > 0:
                    print(f"\n   ... und {remaining} weitere Routen")
                break
    else:
        print("❌ Keine Routen gefunden.")
    
    print("\n" + "="*70 + "\n")
    
    # 3. Demonstration der Route-Erstellung für heute
    print("3. NEUE ROUTE FÜR HEUTE ERSTELLEN:")
    print("-" * 50)
    
    heute = str(datetime.date.today())
    test_coordinates = [
        ("50.7421 7.0660", "2025-01-07 08:00:00+00:00"),
        ("50.7422 7.0661", "2025-01-07 08:01:00+00:00"),
        ("50.7423 7.0662", "2025-01-07 08:02:00+00:00")
    ]
    
    print(f"Erstelle Test-Route für {heute}...")
    route_filename = f"demo-route-{datetime.datetime.now().strftime('%H-%M-%S')}.json"
    
    try:
        for coords, timestamp in test_coordinates:
            dateifunktionen.gps_json_write(coords, timestamp, folder=heute, filename=route_filename)
        
        route_path = os.path.join(heute, route_filename)
        print(f"✅ Test-Route erfolgreich erstellt: {route_path}")
        
        # Zeige die neue Route in der Liste
        print("\nAktualisierte Routenliste:")
        neue_routen = dateifunktionen.get_all_routes_sorted()
        if neue_routen:
            print(f"Neueste Route: {neue_routen[0]['display_name']}")
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen der Test-Route: {e}")

if __name__ == "__main__":
    main()
