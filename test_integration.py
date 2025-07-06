#!/usr/bin/env python3
"""
Test script to verify the map integration works properly
"""

import sys
import os

# Add the GUI directory to the path
gui_path = os.path.join(os.path.dirname(__file__), 'GUI')
sys.path.insert(0, gui_path)

try:
    print("Testing imports...")
    
    # Test tkinter
    import tkinter as tk
    print("✓ tkinter imported successfully")
    
    # Test tkintermapview
    import tkintermapview
    print("✓ tkintermapview imported successfully")
    
    # Test dateifunktionen
    import dateifunktionen
    print("✓ dateifunktionen imported successfully")
    
    # Test our map widget
    from GUI.map_widget import MapWidget
    print("✓ MapWidget imported successfully")
    
    # Test the main app
    from GUI.mainapp import mainappclass
    print("✓ mainappclass imported successfully")
    
    print("\nAll imports successful! The application should work properly.")
    print("You can now run: python GUI/main.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install missing dependencies.")
except Exception as e:
    print(f"❌ Error: {e}")
