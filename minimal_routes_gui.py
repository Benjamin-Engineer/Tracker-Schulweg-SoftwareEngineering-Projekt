#!/usr/bin/env python3
"""
Minimale GUI zum Testen der Routen-Anzeige
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
from pathlib import Path

# Setup paths
project_dir = Path(__file__).parent
gui_dir = project_dir / "GUI"
sys.path.append(str(project_dir))

import dateifunktionen

class MinimalRoutesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Routen Test")
        self.root.geometry("800x600")
        
        # Routen-Liste
        self.setup_ui()
        self.load_routes()
    
    def setup_ui(self):
        """Setup der GUI"""
        # Titel
        title_label = tk.Label(self.root, text="Verfügbare Routen", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame für Liste
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.routes_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            height=20
        )
        self.routes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.routes_listbox.yview)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        view_btn = tk.Button(button_frame, text="Route anzeigen", command=self.view_route)
        view_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(button_frame, text="Aktualisieren", command=self.load_routes)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Info-Text
        self.info_text = tk.Text(self.root, height=8, width=80)
        self.info_text.pack(fill="x", padx=20, pady=10)
    
    def load_routes(self):
        """Lade alle verfügbaren Routen"""
        try:
            self.routes_listbox.delete(0, tk.END)
            self.route_files = []
            
            # Lade Routen
            all_routes = dateifunktionen.get_all_routes_sorted(str(project_dir))
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Gefunden: {len(all_routes)} Routen\n\n")
            
            for i, route_info in enumerate(all_routes):
                display_name = route_info['display_name']
                file_path = route_info['file_path']
                
                self.routes_listbox.insert(tk.END, f"{i+1}. {display_name}")
                self.route_files.append(file_path)
                
                # Info hinzufügen
                exists = os.path.exists(file_path)
                self.info_text.insert(tk.END, f"Route {i+1}: {exists}\n")
                
            self.info_text.insert(tk.END, f"\nRouten erfolgreich geladen!")
            
        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Fehler beim Laden: {e}")
            import traceback
            self.info_text.insert(tk.END, f"\n\n{traceback.format_exc()}")
    
    def view_route(self):
        """Zeige Details der ausgewählten Route"""
        selection = self.routes_listbox.curselection()
        if not selection:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "Bitte wählen Sie eine Route aus!")
            return
        
        try:
            index = selection[0]
            route_file = self.route_files[index]
            selected_text = self.routes_listbox.get(index)
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Ausgewählte Route: {selected_text}\n")
            self.info_text.insert(tk.END, f"Datei: {route_file}\n")
            self.info_text.insert(tk.END, f"Datei existiert: {os.path.exists(route_file)}\n\n")
            
            # Lade Route-Punkte
            route_points = dateifunktionen.routendatei_zu_liste(route_file)
            self.info_text.insert(tk.END, f"Route-Punkte: {len(route_points) if route_points else 0}\n")
            
            if route_points:
                self.info_text.insert(tk.END, f"Erster Punkt: {route_points[0]}\n")
                self.info_text.insert(tk.END, f"Letzter Punkt: {route_points[-1]}\n")
                
                # Zeige erste 5 Punkte
                self.info_text.insert(tk.END, "\nErste 5 Punkte:\n")
                for i, point in enumerate(route_points[:5]):
                    self.info_text.insert(tk.END, f"  {i+1}: {point}\n")
                    
            self.info_text.insert(tk.END, "\n✅ Route erfolgreich geladen!")
            
        except Exception as e:
            self.info_text.insert(tk.END, f"\n❌ Fehler beim Anzeigen: {e}")
            import traceback
            self.info_text.insert(tk.END, f"\n\n{traceback.format_exc()}")

def main():
    root = tk.Tk()
    app = MinimalRoutesGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
