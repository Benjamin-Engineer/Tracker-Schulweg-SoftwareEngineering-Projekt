#!/usr/bin/env python3
"""
Diagnose-Skript für die GUI Routen-Anzeige Probleme
"""

import os
import sys
from pathlib import Path

# Füge das Projektverzeichnis zum Python-Pfad hinzu
project_dir = Path(__file__).parent
sys.path.append(str(project_dir))

import dateifunktionen

def diagnose_routes():
    print("=== DIAGNOSE DER ROUTEN-ANZEIGE PROBLEME ===\n")
    
    # 1. Teste die dateifunktionen direkt
    print("1. TESTE DATEIFUNKTIONEN:")
    print("-" * 40)
    
    try:
        all_routes = dateifunktionen.get_all_routes_sorted()
        print(f"✅ get_all_routes_sorted() erfolgreich: {len(all_routes)} Routen gefunden")
        
        for i, route in enumerate(all_routes[:3]):  # Zeige nur die ersten 3
            print(f"  Route {i+1}:")
            print(f"    Display Name: {route['display_name']}")
            print(f"    File Path: {route['file_path']}")
            print(f"    Datei existiert: {os.path.exists(route['file_path'])}")
            
            # Teste routendatei_zu_liste
            if os.path.exists(route['file_path']):
                try:
                    route_points = dateifunktionen.routendatei_zu_liste(route['file_path'])
                    print(f"    Route-Punkte: {len(route_points) if route_points else 0}")
                except Exception as e:
                    print(f"    ❌ Fehler beim Laden der Route-Punkte: {e}")
            print()
            
    except Exception as e:
        print(f"❌ Fehler bei get_all_routes_sorted(): {e}")
    
    print("\n" + "="*60 + "\n")
    
    # 2. Teste den GUI-Pfad
    print("2. TESTE GUI-PFAD STRUKTUR:")
    print("-" * 40)
    
    gui_dir = project_dir / "GUI"
    print(f"GUI Verzeichnis: {gui_dir}")
    print(f"GUI Verzeichnis existiert: {gui_dir.exists()}")
    
    if gui_dir.exists():
        gui_files = list(gui_dir.glob("*.py"))
        print(f"Python-Dateien in GUI: {[f.name for f in gui_files]}")
    
    # Teste relative Pfade von GUI aus
    parent_from_gui = gui_dir.parent
    print(f"Parent von GUI: {parent_from_gui}")
    print(f"Parent entspricht Projekt: {parent_from_gui == project_dir}")
    
    print("\n" + "="*60 + "\n")
    
    # 3. Simuliere GUI-Import
    print("3. SIMULIERE GUI-IMPORT:")
    print("-" * 40)
    
    try:
        # Simuliere das, was die GUI macht
        base_dir = gui_dir.parent  # Parent Verzeichnis
        
        if str(base_dir) not in sys.path:
            sys.path.append(str(base_dir))
            print(f"✅ Pfad hinzugefügt: {base_dir}")
        
        # Versuche Import
        import dateifunktionen as df_gui
        print("✅ dateifunktionen Import erfolgreich")
        
        # Teste Funktionen
        routes_from_gui = df_gui.get_all_routes_sorted(str(base_dir))
        print(f"✅ get_all_routes_sorted() von GUI: {len(routes_from_gui)} Routen")
        
        # Teste Pfad-Konvertierung
        for route in routes_from_gui[:2]:
            file_path = route['file_path']
            if not os.path.isabs(file_path):
                abs_path = os.path.join(str(base_dir), file_path)
                print(f"Relativer Pfad: {file_path}")
                print(f"Absoluter Pfad: {abs_path}")
                print(f"Datei existiert (relativ): {os.path.exists(file_path)}")
                print(f"Datei existiert (absolut): {os.path.exists(abs_path)}")
            else:
                print(f"Bereits absoluter Pfad: {file_path}")
                print(f"Datei existiert: {os.path.exists(file_path)}")
            print()
            
    except Exception as e:
        print(f"❌ Fehler bei GUI-Simulation: {e}")
        import traceback
        traceback.print_exc()

def test_route_display():
    print("\n4. TESTE ROUTEN-ANZEIGE:")
    print("-" * 40)
    
    try:
        routes = dateifunktionen.get_all_routes_sorted()
        if routes:
            test_route = routes[0]
            route_file = test_route['file_path']
            
            print(f"Teste Route: {test_route['display_name']}")
            print(f"Route-Datei: {route_file}")
            
            # Lade Route-Punkte
            route_points = dateifunktionen.routendatei_zu_liste(route_file)
            print(f"Route-Punkte geladen: {len(route_points) if route_points else 0}")
            
            if route_points:
                print("Erste 3 Punkte:")
                for i, point in enumerate(route_points[:3]):
                    print(f"  {i+1}: {point}")
            
            # Teste Standorte für diese Route
            standorte = dateifunktionen.get_standorte(routendatei=route_file)
            print(f"Standorte für Route: {len(standorte)}")
            
        else:
            print("❌ Keine Routen für Test verfügbar")
            
    except Exception as e:
        print(f"❌ Fehler beim Testen der Routen-Anzeige: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_routes()
    test_route_display()
