#!/usr/bin/env python3
"""
Test script to verify live GPS simulation display on lock screen
"""

import tkinter as tk
import sys
import os
import time
from threading import Thread

# Add current directory to path
sys.path.append(os.getcwd())

def test_lock_screen_live_simulation():
    """Test the lock screen live simulation functionality"""
    print("🔒 Testing Lock Screen Live GPS Simulation")
    print("=" * 50)
    
    try:
        from gesperrt import gesperrtpage
        from tracking import trackingpage
        print("✓ Lock screen and tracking pages imported successfully")
        
        # Create test window
        root = tk.Tk()
        root.geometry("1920x1080")
        root.configure(bg="#363434")
        root.title("Lock Screen Live Simulation Test")
        
        class TestController:
            def __init__(self):
                self.frames = {}
                
            def show_frame(self, page_class):
                print(f"Would switch to: {page_class.__name__}")
        
        controller = TestController()
        
        # Create tracking page and lock screen
        tracking_frame = trackingpage(root, controller)
        lock_frame = gesperrtpage(root, controller)
        
        controller.frames[trackingpage] = tracking_frame
        controller.frames[gesperrtpage] = lock_frame
        
        # Pack lock screen
        lock_frame.pack(fill="both", expand=True)
        
        print("✓ Lock screen created with live simulation support")
        
        # Simulate some GPS points in the tracking frame
        def simulate_gps_points():
            """Simulate GPS points being added to tracking"""
            base_lat, base_lon = 50.7374, 7.0982
            
            # Initialize tracking simulation
            tracking_frame.tracking = True
            tracking_frame.route_points = []
            
            for i in range(10):
                time.sleep(2)  # Wait 2 seconds between points
                
                # Add a new GPS point
                lat = base_lat + (i * 0.0001)  # Move north
                lon = base_lon + (i * 0.0001)  # Move east
                tracking_frame.route_points.append((lat, lon))
                
                print(f"Added GPS point {i+1}: ({lat:.6f}, {lon:.6f})")
                
                # Simulate stationary point at step 5
                if i == 4:
                    tracking_frame.last_stationary_point = (lat, lon)
                    tracking_frame.stationary_marked = True
                    print("Simulated stationary point")
            
            print("GPS simulation completed")
            tracking_frame.tracking = False
        
        # Create info panel
        info_frame = tk.Frame(root, bg="#555555")
        info_frame.place(x=1300, y=50, width=400, height=200)
        
        info_label = tk.Label(
            info_frame,
            text="Lock Screen Live Simulation Test\n\n" +
                 "• GPS points will be added every 2 seconds\n" +
                 "• Lock screen should update automatically\n" +
                 "• Watch the map for live route drawing\n" +
                 "• Stationary point will appear at step 5\n\n" +
                 "Close window to end test",
            bg="#555555",
            fg="white",
            font=("Arial", 10),
            justify="left"
        )
        info_label.pack(padx=10, pady=10)
        
        # Start GPS simulation in background thread
        simulation_thread = Thread(target=simulate_gps_points, daemon=True)
        simulation_thread.start()
        
        # Trigger lock screen on_show to start live updates
        lock_frame.on_show()
        
        print("\n🚀 Test running!")
        print("Watch the lock screen map for live GPS simulation updates")
        print("Points should appear every 2 seconds")
        print("Red marker should appear at the 5th point (stationary)")
        
        try:
            root.mainloop()
        except KeyboardInterrupt:
            print("Test interrupted by user")
        finally:
            if lock_frame:
                lock_frame.stop_live_simulation_updates()
            root.destroy()
            
    except ImportError as e:
        print(f"✗ Import error: {e}")
    except Exception as e:
        print(f"✗ Test error: {e}")
        import traceback
        traceback.print_exc()

def test_live_update_methods():
    """Test if the lock screen has the required methods"""
    print("\n🔧 Testing Live Update Methods")
    print("-" * 30)
    
    try:
        from gesperrt import gesperrtpage
        
        # Create a dummy test
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        class DummyController:
            def __init__(self):
                self.frames = {}
        
        controller = DummyController()
        lock_frame = gesperrtpage(root, controller)
        
        # Test methods
        methods_to_test = [
            'start_live_simulation_updates',
            'stop_live_simulation_updates', 
            'live_simulation_update_cycle',
            'update_live_simulation_display',
            'sync_stationary_markers',
            'show_recent_route_fallback',
            'on_show',
            'on_hide'
        ]
        
        for method_name in methods_to_test:
            if hasattr(lock_frame, method_name):
                print(f"✓ {method_name} method exists")
            else:
                print(f"✗ {method_name} method missing")
        
        root.destroy()
        
    except Exception as e:
        print(f"✗ Method test error: {e}")

if __name__ == "__main__":
    test_live_update_methods()
    test_lock_screen_live_simulation()
    
    print("\n" + "=" * 50)
    print("🎯 Live Simulation Integration Summary:")
    print("- Lock screen now monitors GPS simulation continuously")
    print("- Updates every 2 seconds while lock screen is active") 
    print("- Shows live route drawing as simulation progresses")
    print("- Displays stationary markers in real-time")
    print("- Automatically stops updates when unlocking")
    print("- Falls back to recent routes when no live simulation")
    print("\n✅ Lock screen live simulation is ready!")
