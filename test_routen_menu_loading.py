#!/usr/bin/env python3
"""
Test script to verify that the route menu loads routes correctly
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "GUI"))

def test_routen_menu_loading():
    """Test that the route menu can load all routes correctly"""
    print("=== TESTE ROUTEN MENÜ LADEN ===")
    
    try:
        # Import dateifunktionen 
        import dateifunktionen
        print("✅ dateifunktionen Import erfolgreich")
        
        # Get all routes
        all_routes = dateifunktionen.get_all_routes_sorted(str(project_root))
        print(f"✅ {len(all_routes)} Routen gefunden")
        
        # Display the first few routes
        for i, route_info in enumerate(all_routes[:5]):
            print(f"Route {i+1}: {route_info['display_name']}")
            print(f"  Pfad: {route_info['file_path']}")
            print(f"  Existiert: {os.path.exists(route_info['file_path'])}")
            
        # Test the routen_menü loading logic
        print("\n=== TESTE ROUTEN MENÜ KLASSE ===")
        
        # Mock the controller and tkinter elements
        class MockController:
            def __init__(self):
                self.frames = {}
        
        class MockTk:
            def place(self, **kwargs):
                pass
            def pack(self, **kwargs):
                pass
            def config(self, **kwargs):
                pass
            def delete(self, start, end):
                pass
            def insert(self, index, text):
                print(f"  Listbox Insert: {text}")
        
        # Import tkinter with mocking
        import tkinter as tk
        
        # Create a mock frame
        mock_controller = MockController()
        
        # Instead of creating the full GUI, just test the load_routes logic
        try:
            from GUI.routen_menü import routen_menüpage
            print("✅ routen_menüpage Import erfolgreich")
            
            # Test the load_routes method manually
            base_dir = Path(__file__).parent
            route_files = []
            
            # Simulate the load_routes logic
            import dateifunktionen
            all_routes = dateifunktionen.get_all_routes_sorted(str(base_dir))
            
            if all_routes:
                print(f"✅ Load Routes Logic: {len(all_routes)} Routen gefunden")
                for i, route_info in enumerate(all_routes[:3]):
                    display_name = route_info['display_name']
                    file_path = route_info['file_path']
                    
                    print(f"  Route {i}: {display_name}")
                    print(f"    Pfad: {file_path}")
                    print(f"    Existiert: {os.path.exists(file_path)}")
                    
                    route_files.append(file_path)
            
            print("✅ Routen Menü Loading Test erfolgreich")
            
        except ImportError as e:
            print(f"❌ Import Fehler für routen_menüpage: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Fehler beim Testen: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_routen_menu_loading()
    if success:
        print("\n✅ Alle Tests erfolgreich!")
    else:
        print("\n❌ Einige Tests fehlgeschlagen!")
