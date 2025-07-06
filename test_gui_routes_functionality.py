#!/usr/bin/env python3
"""
Teste die GUI Routen-Funktionalität direkt
"""

import sys
import os
from pathlib import Path

# Setup paths
project_dir = Path(__file__).parent
gui_dir = project_dir / "GUI"
sys.path.append(str(project_dir))

def test_gui_route_loading():
    """Teste das Laden der Routen wie in der GUI"""
    print("=== TESTE GUI ROUTEN-LADEN ===\n")
    
    # Simuliere GUI-Umgebung
    base_dir = gui_dir.parent
    print(f"Base Directory: {base_dir}")
    
    if str(base_dir) not in sys.path:
        sys.path.append(str(base_dir))
        print(f"Pfad hinzugefügt: {base_dir}")
    
    try:
        import dateifunktionen
        print("✅ dateifunktionen Import erfolgreich")
        
        # Lade Routen wie in der GUI
        all_routes = dateifunktionen.get_all_routes_sorted(str(base_dir))
        print(f"✅ {len(all_routes)} Routen geladen")
        
        # Simuliere GUI Listbox-Füllung
        routes_listbox_items = []
        route_files = []
        
        for i, route_info in enumerate(all_routes):
            display_name = route_info['display_name']
            file_path = route_info['file_path']
            
            print(f"\nRoute {i+1}:")
            print(f"  Display: {display_name}")
            print(f"  Pfad: {file_path}")
            print(f"  Datei existiert: {os.path.exists(file_path)}")
            
            routes_listbox_items.append(display_name)
            route_files.append(file_path)
        
        print(f"\n=== SIMULATION EINER ROUTE-AUSWAHL ===")
        if route_files:
            # Simuliere Auswahl der ersten Route
            selected_index = 0
            selected_route = route_files[selected_index]
            selected_display = routes_listbox_items[selected_index]
            
            print(f"Simuliere Auswahl von Route {selected_index}:")
            print(f"  Display: {selected_display}")
            print(f"  Datei: {selected_route}")
            print(f"  Datei existiert: {os.path.exists(selected_route)}")
            
            # Teste routendatei_zu_liste
            try:
                route_points = dateifunktionen.routendatei_zu_liste(selected_route)
                print(f"  Route-Punkte: {len(route_points) if route_points else 0}")
                if route_points:
                    print(f"  Erster Punkt: {route_points[0]}")
                    print(f"  Letzter Punkt: {route_points[-1]}")
            except Exception as e:
                print(f"  ❌ Fehler beim Laden der Route-Punkte: {e}")
            
            # Teste zweite Route falls vorhanden
            if len(route_files) > 1:
                print(f"\nSimuliere Auswahl von Route 1:")
                selected_route_2 = route_files[1]
                selected_display_2 = routes_listbox_items[1]
                print(f"  Display: {selected_display_2}")
                print(f"  Datei: {selected_route_2}")
                print(f"  Datei existiert: {os.path.exists(selected_route_2)}")
                
                try:
                    route_points_2 = dateifunktionen.routendatei_zu_liste(selected_route_2)
                    print(f"  Route-Punkte: {len(route_points_2) if route_points_2 else 0}")
                    if route_points_2:
                        print(f"  Erster Punkt: {route_points_2[0]}")
                        print(f"  Letzter Punkt: {route_points_2[-1]}")
                except Exception as e:
                    print(f"  ❌ Fehler beim Laden der Route-Punkte: {e}")
        
        print(f"\n✅ GUI Routen-Test erfolgreich abgeschlossen")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui_route_loading()
