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

    new_entry = {
        "coord": coordinates_str,
        "time": timestamp_str
    }
    existing_data.append(new_entry)
    try:
        with open(full_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        print(f"Eintrag erfolgreich zu {full_path} hinzugefügt.")
    except IOError as e:
        print(f"Fehler beim Schreiben in Datei {full_path}: {e}")