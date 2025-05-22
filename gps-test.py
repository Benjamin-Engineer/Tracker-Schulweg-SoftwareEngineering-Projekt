import datetime
from dateifunktionen import gps_json_write #Custom Import. Kann kaputtgehen wenn die Routendatei umbenannt wird


def load_data_from_file(filepath):
    """Liest Daten aus einer angegebenen .txt-Datei aus und gibt sie als Liste zurück, die von "dateifunktionen" verwendet werden kann.
    Ausgabeformat: [coords, timestamp, coords, timestamp, ...].
    Beispiel:
    ["50.74271683333333 7.0670345",
    "2025-05-21 20:04:28+00.00",
    "50.74271683333333 7.0670345",
    "2025-05-21 20:04:29+00.00"]
    usw.
    """
    new_data_list = []
    try:
        with open(filepath, 'r') as f:
            # Read all lines, strip whitespace, and filter out empty lines
            lines = [line.strip() for line in f if line.strip()]

        # Process lines in pairs: testdaten.txt has date, then coords.
        # The target 'daten' list structure is: coords, then timestamp.
        idx = 0
        while idx + 1 < len(lines):
            date_str = lines[idx]      # e.g., "2025-05-21 20:04:28+00.00"
            coords_str = lines[idx+1]  # e.g., "50.74271683333333 7.0670345"

            new_data_list.append(coords_str)
            new_data_list.append(date_str)

            idx += 2
    except FileNotFoundError:
        print(f"Warning: File '{filepath}' not found. 'daten' will be empty.")
    except Exception as e:
        print(f"An error occurred while reading '{filepath}': {e}. 'daten' will be empty.")
    return new_data_list

# Load data from testdaten.txt instead of using a hardcoded list
listendatei = "testdaten.txt"
daten = load_data_from_file(listendatei) # testdaten.txt muss sich im gleichen Ordner wie gps-test.py befinden


def gps_test(data_list):
    # Using enumerate for a cleaner loop
    for i, item in enumerate(data_list):
        print(i, item)

# Gibt die Liste der Daten über print() aus. Nummerierung ist in der json nicht vorhanden
if daten:
    gps_test(daten)
else:
    print(listendatei, "enthält keine Daten.")




# Ordner der Routendatei
# Wenn der Ordner nicht existiert, wird er erstellt
parent_folder = str(datetime.date.today())
"""
Fügt alle Koordinaten-Paare aus der Liste 'daten' mit den zugehörigen Zeitstempeln (aus testdaten.txt generiert) zur Route in der Datei hinzu.
Ist keine Datei angegeben oder existiert die angegeben Datei nicht, wird automatisch eine neue Datei mit aktueller Zeit als Namen erstellt.
"""
if daten:
    for i in range(0, len(daten), 2):
        coords_str = daten[i]
        time_str = daten[i+1]

# BEISPIELE (Hasttag entfernen zum ausprobieren):
        gps_json_write(coords_str, time_str, parent_folder) # Erzeugt eine neue Datei mit aktueller Zeit als Namen im Ordner parent_folder.
        #gps_json_write(coords_str, time_str) # Erzeugt eine neue Datei im gleichen Ordner wie dieses Programm
        #gps_json_write (coords, time_str, parent_folder, "Name") # Erzeugt eine neue Datei Name.json in parent_folder
        #gps_json_write (coords, time_str, "Name") # Erzeugt eine neue Datei Name.json im gleichen Ordner
        #gps_json_write (coords, time_str, "Beispielordner", "Name") # Erzeugt eine neue Datei Name.json im Ordner Beispielordner