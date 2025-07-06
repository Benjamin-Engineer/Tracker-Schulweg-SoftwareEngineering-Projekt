#!/usr/bin/env python3
"""
Test script to verify that route switching works correctly in the GUI.
This will create test routes with different GPS points and simulate the route switching process.
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_route(folder_name, file_name, start_lat, start_lon, num_points=10):
    """Create a test route file with GPS points"""
    
    # Create date folder if it doesn't exist
    folder_path = Path(folder_name)
    folder_path.mkdir(exist_ok=True)
    
    route_file = folder_path / file_name
    
    route_data = []
    
    # Generate GPS points in a line
    for i in range(num_points):
        lat = start_lat + (i * 0.001)  # Move north
        lon = start_lon + (i * 0.001)  # Move east
        
        timestamp = datetime.now() + timedelta(seconds=i*10)
        
        # Use the correct format that matches existing route files
        point_data = {
            "coord": f"{lat:.6f} {lon:.6f}",
            "time": timestamp.strftime("%Y-%m-%d %H:%M:%S+00:00")
        }
        route_data.append(point_data)
    
    # Write route data to JSON file
    with open(route_file, 'w') as f:
        json.dump(route_data, f, indent=2)
    
    print(f"Created test route: {route_file}")
    print(f"  Start: ({start_lat:.6f}, {start_lon:.6f})")
    print(f"  End: ({start_lat + (num_points-1)*0.001:.6f}, {start_lon + (num_points-1)*0.001:.6f})")
    print(f"  Points: {num_points}")
    
    return str(route_file)

def test_route_switching():
    """Test route switching functionality"""
    print("=== Testing Route Switching Fix ===\n")
    
    # Create 3 different test routes
    routes = []
    
    # Route 1: Bonn area
    route1 = create_test_route(
        "2025-01-01", 
        "2025-01-01 10-00-00-000000.json",
        50.7374, 7.0982, 8
    )
    routes.append(route1)
    
    # Route 2: Different area in Bonn
    route2 = create_test_route(
        "2025-01-02", 
        "2025-01-02 14-30-00-000000.json",
        50.7500, 7.1100, 6
    )
    routes.append(route2)
    
    # Route 3: Another different area
    route3 = create_test_route(
        "2025-01-03", 
        "2025-01-03 16-15-00-000000.json",
        50.7300, 7.0800, 12
    )
    routes.append(route3)
    
    print(f"\nCreated {len(routes)} test routes\n")
    
    # Test dateifunktionen
    try:
        import dateifunktionen
        
        print("Testing dateifunktionen.get_all_routes_sorted():")
        all_routes = dateifunktionen.get_all_routes_sorted(".")
        
        if all_routes:
            print(f"Found {len(all_routes)} routes:")
            for i, route_info in enumerate(all_routes):
                print(f"  {i+1}. {route_info['display_name']} -> {route_info['file_path']}")
                
                # Verify route content
                route_points = dateifunktionen.routendatei_zu_liste(route_info['file_path'])
                if route_points:
                    print(f"     {len(route_points)} GPS points: {route_points[0]} to {route_points[-1]}")
                else:
                    print(f"     ERROR: No GPS points found!")
        else:
            print("  No routes found")
        
    except Exception as e:
        print(f"Error testing dateifunktionen: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Instructions for Manual GUI Testing ===")
    print("1. Run the main GUI application")
    print("2. Go to Routen menu")
    print("3. You should see 3 test routes in the list")
    print("4. Select the first route and click 'Einklappen' (view route)")
    print("5. Verify the route is displayed on the map")
    print("6. Go back to Routen menu")
    print("7. Select the second route and click 'Einklappen'")
    print("8. The map should now show the SECOND route, not the first one")
    print("9. Repeat with the third route")
    print("\nIf the map always shows the same route regardless of selection,")
    print("the bug is still present. If it shows different routes, the fix works!")
    
    return routes

if __name__ == "__main__":
    test_routes = test_route_switching()
    
    print(f"\nTest routes created:")
    for i, route in enumerate(test_routes, 1):
        print(f"  Route {i}: {route}")
