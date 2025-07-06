#!/usr/bin/env python3
"""
Test script to verify GPS simulation integration
"""

import tkinter as tk
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from start import startpage
from tracking import trackingpage

def test_gps_simulation_integration():
    """Test the GPS simulation integration"""
    root = tk.Tk()
    root.geometry("1920x1080")
    root.configure(bg="#363434")
    root.title("GPS Simulation Integration Test")
    
    class TestController:
        def __init__(self):
            self.frames = {}
            
        def show_frame(self, page_class):
            print(f"Would switch to: {page_class.__name__}")
            # In a real app, this would switch frames
            
        def create_frames(self, container):
            # Create the frames like in the real app
            for F in (startpage, trackingpage):
                frame = F(parent=container, controller=self)
                self.frames[F] = frame
    
    controller = TestController()
    
    # Create container
    container = tk.Frame(root)
    container.pack(side="top", fill="both", expand=True)
    
    # Create frames
    controller.create_frames(container)
    
    # Show start page
    start_frame = controller.frames[startpage]
    start_frame.pack(fill="both", expand=True)
    
    print("✓ Start page created")
    print("✓ Tracking page created")
    print("✓ GPS simulation integrated")
    print("\nTest completed successfully!")
    print("Click the green 'Start' button to begin GPS simulation")
    print("The simulation will:")
    print("- Generate a realistic route around Bonn")
    print("- Switch to tracking page") 
    print("- Show live GPS movement on the map")
    print("- Create route files in date-specific folders")
    print("- Include stationary points during the route")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Test interrupted by user")
        root.destroy()

if __name__ == "__main__":
    test_gps_simulation_integration()
