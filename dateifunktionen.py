import json
import os # path operations & folder creation
from datetime import datetime


def gps_json_write(coordinates_str, timestamp_str,  folder=".", filename=str(datetime.now()).replace(":", "-").replace(".", "-") + ".json"):
    """
    Fügt einen neuen Eintrag (Koordinaten und Zeit) zu einer JSON-Datei hinzu.
    Wenn die Datei nicht existiert, wird eine neue erstellt.
    Falls die Datei leer ist, wird eine neue Liste erstellt.

    Falls nicht angegeben: Dateiname = YYYY-MM-DD HH-MM-SS.json, Ordner = selber Ordner wie Program

    Args:
        coordinates_str (str): Die Koordinaten als String (z.B. "50.74270766666667 7.066976833333333").
        timestamp_str (str): Der Zeitstempel als String. (z.B.2025-05-21 20:04:28+00.00)
        filename (str): Der Name der JSON-Datei (z.B. "23-22-21.json").
        folder (str, optional): Der Ordner, in dem die Datei gespeichert werden soll. Standardmäßig der aktuelle Ordner (".").
    """

    original_coordinates_str = coordinates_str  # Keep for messages

    final_coord_str_to_write = original_coordinates_str  # Default if not parsable
    current_f_lat, current_f_lon = None, None
    is_current_coord_valid_for_comparison = False

    # Attempt to parse original_coordinates_str and format to 6 decimal places. (6 Nachkommastellen sind auf 0.11112m genau, laut https://wiki.openstreetmap.org/wiki/Precision_of_coordinates)
    # Also, get float versions of these 6-decimal-place values for comparison.
    try:
        raw_lat_str, raw_lon_str = original_coordinates_str.split()
        raw_lat = float(raw_lat_str)
        raw_lon = float(raw_lon_str)
        
        final_coord_str_to_write = f"{raw_lat:.6f} {raw_lon:.6f}"
        current_f_lat = float(f"{raw_lat:.6f}") # Float from 6-decimal representation
        current_f_lon = float(f"{raw_lon:.6f}") # Float from 6-decimal representation
        is_current_coord_valid_for_comparison = True
    except ValueError:
        print (f"Info: Eingabe '{original_coordinates_str}' enthält keine validen Koordinaten und wird unaufbereitet übernommen.")

    # Ensure the target folder exists, create it if it doesn't
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            print(f"Info: Ordner '{folder}' wurde erstellt.")
        except OSError as e:
            print(f"Fehler: Konnte Ordner '{folder}' nicht erstellen: {e}")
            return # Exit if folder creation fails

    full_path = os.path.join(folder, filename)
    existing_data = []

    try:
        with open(full_path, 'r') as f:
            loaded_data = json.load(f)
            if isinstance(loaded_data, list):
                existing_data = loaded_data
            else:
                print(f"Warnung: Datei {full_path} enthielt keine Liste. Eine neue Liste wird erstellt.")
    except FileNotFoundError:
        print(f"Info: Datei {full_path} nicht gefunden. Eine neue Datei wird erstellt.")
    except json.JSONDecodeError:
        print(f"Warnung: Datei {full_path} enthielt ungültiges JSON oder war leer. Eine neue Liste wird erstellt.")

    # Check for deviation if current coordinates are valid for comparison and there's previous data
    if is_current_coord_valid_for_comparison and existing_data:
        last_entry = existing_data[-1]
        last_coords_str_from_file = last_entry.get("coord")

        if last_coords_str_from_file:
            try:
                # Previous coordinates from file (should already be 6dp if valid)
                last_lat_str_ff, last_lon_str_ff = last_coords_str_from_file.split() # ff = from file
                last_f_lat = float(last_lat_str_ff)
                last_f_lon = float(last_lon_str_ff)



                culling_accuracy = 0.00001 # 0.00001 = 0.11112m <-> 0.0001 = 1.1112m <-> 0.001 = 11.112m (laut https://wiki.openstreetmap.org/wiki/Precision_of_coordinates)

                if abs(current_f_lat - last_f_lat) < culling_accuracy and abs(current_f_lon - last_f_lon) < culling_accuracy:
                    print(f"Info: Neuer Eintrag (Original: '{original_coordinates_str}', Formatiert: '{final_coord_str_to_write}') weicht minimal von letztem Eintrag ('{last_coords_str_from_file}') ab. Eintrag wird übersprungen.")
                    return # Do not add the new entry
            except ValueError:
                # Last coordinate in file was not a valid parsable pair (e.g., "NO SIGNAL").
                # Proceed to add the new one if it's valid.
                pass

    new_entry = {
        "coord": final_coord_str_to_write,
        "time": timestamp_str
    }
    existing_data.append(new_entry)
    try:
        with open(full_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        print(f"Eintrag erfolgreich zu {full_path} hinzugefügt.")
    except IOError as e:
        print(f"Fehler beim Schreiben in Datei {full_path}: {e}")