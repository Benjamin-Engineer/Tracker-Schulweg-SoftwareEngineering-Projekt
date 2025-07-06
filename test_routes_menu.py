#!/usr/bin/env python3
"""
Isolierter Test für das Routen-Menü
"""

import tkinter as tk
import sys
import os
from pathlib import Path

# Füge die Pfade hinzu
project_dir = Path(__file__).parent
gui_dir = project_dir / "GUI"
sys.path.append(str(project_dir))
sys.path.append(str(gui_dir))

class TestController:
    """Einfacher Controller für den Test"""
    def __init__(self):
        self.frames = {}
    
    def show_frame(self, frame_class):
        print(f"Controller: Wechsle zu {frame_class.__name__}")

def test_routes_menu():
    """Teste das Routen-Menü isoliert"""
    print("=== TESTE ROUTEN-MENÜ ISOLIERT ===")
    
    # Erstelle Tkinter Root
    root = tk.Tk()
    root.title("Routen-Menü Test")
    root.geometry("1920x1080")
    
    # Erstelle Test-Controller
    controller = TestController()
    
    try:
        # Importiere das Routen-Menü
        from routen_menü import routen_menüpage
        
        # Erstelle das Routen-Menü
        routes_menu = routen_menüpage(root, controller)
        routes_menu.pack(fill="both", expand=True)
        
        print("✅ Routen-Menü erfolgreich erstellt")
        
        # Starte GUI-Loop
        print("GUI gestartet. Schließen Sie das Fenster, um den Test zu beenden.")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Fehler beim Erstellen des Routen-Menüs: {e}")
        import traceback
        traceback.print_exc()
        root.destroy()

if __name__ == "__main__":
    test_routes_menu()
