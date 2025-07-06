#!/usr/bin/env python3
"""
Test script to verify that the lock screen map integration works
"""

import tkinter as tk
from gesperrt import gesperrtpage

def test_lock_screen_map():
    """Test the lock screen with map integration"""
    root = tk.Tk()
    root.geometry("1920x1080")
    root.configure(bg="#363434")
    root.title("Lock Screen Map Test")
    
    # Create a dummy controller
    class DummyController:
        def show_frame(self, page_class):
            print(f"Would show frame: {page_class}")
    
    controller = DummyController()
    
    # Create the lock screen page
    lock_screen = gesperrtpage(root, controller)
    lock_screen.pack(fill="both", expand=True)
    
    # Trigger the on_show method to load map data
    lock_screen.on_show()
    
    print("Lock screen with map created successfully!")
    print("You should see the map on the left side of the screen.")
    print("Press Ctrl+C or close the window to exit.")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Test interrupted by user")
        root.destroy()

if __name__ == "__main__":
    test_lock_screen_map()
