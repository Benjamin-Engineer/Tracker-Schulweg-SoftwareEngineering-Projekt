#!/usr/bin/env python3
"""
Test für den Sperrmodus mit interaktiver Karte
"""

import tkinter as tk
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from gesperrt import gesperrtpage
    print("✓ gesperrtpage imported successfully")
except ImportError as e:
    print(f"✗ Error importing gesperrtpage: {e}")
    sys.exit(1)

def test_lock_screen_with_map():
    """Test den Sperrmodus mit der neuen interaktiven Karte"""
    
    class TestController:
        """Dummy controller for testing"""
        def show_frame(self, frame_class):
            print(f"Would show frame: {frame_class}")
    
    root = tk.Tk()
    root.geometry("1920x1080")
    root.configure(bg="#363434")
    root.title("Lock Screen with Map Test")
    
    print("Creating lock screen with interactive map...")
    
    # Create test controller
    controller = TestController()
    
    # Create the lock screen page
    lock_page = gesperrtpage(root, controller)
    lock_page.pack(fill="both", expand=True)
    
    print("✓ Lock screen with map created")
    print("You should see:")
    print("  - Interactive map on the left side (1280px wide)")
    print("  - PIN entry and unlock button on the right side")
    print("  - Power button in bottom left")
    print("Use Ctrl+C or close window to exit")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Test interrupted by user")
        root.destroy()

if __name__ == "__main__":
    test_lock_screen_with_map()
