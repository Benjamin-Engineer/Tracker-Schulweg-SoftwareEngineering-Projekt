#!/usr/bin/env python3
"""
Test der Routen-Menü Funktionalität
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'GUI'))

# Import der Routenmenü-Funktionalität
from GUI.routen_menü import routen_menüpage
import tkinter as tk
from datetime import datetime

def test_routes_loading():
    """Einfacher Test der Routen-Lade-Funktionalität"""
    # Mock Controller für den Test
    class MockController:
        def __init__(self):
            self.frames = {}
        
        def show_frame(self, frame_class):
            print(f"Wechsel zu Frame: {frame_class.__name__}")
    
    # Erstelle ein Fenster für den Test
    root = tk.Tk()
    root.geometry("1920x1080")
    root.title("Test - Routen Menü")
    
    controller = MockController()
    
    # Erstelle die Routen-Menü-Seite
    routen_menu = routen_menüpage(root, controller)
    routen_menu.pack(fill="both", expand=True)
    
    print(f"Aktuelles Datum: {datetime.now().strftime('%Y-%m-%d')}")
    print("Routen-Menü geladen. Teste manuell durch Klicken auf 'Routen' Button.")
    
    # Starte die GUI
    root.mainloop()

if __name__ == "__main__":
    test_routes_loading()
