#!/usr/bin/env python3
"""
Simple test to verify map widget works in the lock screen
"""

import tkinter as tk
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from map_widget import MapWidget
    print("✓ MapWidget imported successfully")
except ImportError as e:
    print(f"✗ Error importing MapWidget: {e}")
    sys.exit(1)

def test_simple_map():
    """Test if map widget can be created and displayed"""
    root = tk.Tk()
    root.geometry("1280x1080")
    root.configure(bg="#363434")
    root.title("Simple Map Test")
    
    print("Creating map widget...")
    map_widget = MapWidget(root, width=1280, height=1080)
    map_widget.place(x=0, y=0)
    print("✓ Map widget created and placed")
    
    # Create a simple close button
    close_btn = tk.Button(root, text="Close", command=root.destroy, 
                         bg="red", fg="white", font=("Arial", 16))
    close_btn.place(x=10, y=10)
    
    print("✓ Test window ready!")
    print("You should see a map centered on Bonn, Germany")
    print("Click 'Close' button or use Ctrl+C to exit")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Test interrupted by user")
        root.destroy()

if __name__ == "__main__":
    test_simple_map()
