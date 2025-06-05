import datetime
import dateifunktionen # Benutzerdefinierter Import. Kann fehlschlagen, wenn dateifunktionen.py umbenannt wird.



# Welche Testdatendatei soll verwendet werden?
listendatei = "testdaten_extrapoliert.txt"
#listendatei = "testdaten.txt"



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
            # Alle Zeilen lesen, Leerzeichen entfernen und leere Zeilen herausfiltern
            lines = [line.strip() for line in f if line.strip()]

        # Zeilen paarweise verarbeiten: testdaten.txt enthält Datum, dann Koordinaten.
        # Die Zielstruktur der 'daten'-Liste ist: Koordinaten, dann Zeitstempel.
        idx = 0
        while idx + 1 < len(lines):
            date_str = lines[idx]      # z.B. "2025-05-21 20:04:28+00.00"
            coords_str = lines[idx+1]  # z.B. "50.74271683333333 7.0670345"

            new_data_list.append(coords_str)
            new_data_list.append(date_str)

            idx += 2
    except FileNotFoundError:
        print(f"Warning: File '{filepath}' not found. 'daten' will be empty.")
        # print(f"Warnung: Datei '{filepath}' nicht gefunden. 'daten' wird leer sein.") # Alternative deutsche Meldung
    except Exception as e:
        print(f"An error occurred while reading '{filepath}': {e}. 'daten' will be empty.")
        # print(f"Beim Lesen von '{filepath}' ist ein Fehler aufgetreten: {e}. 'daten' wird leer sein.") # Alternative deutsche Meldung
    return new_data_list

daten = load_data_from_file(listendatei) # testdaten.txt muss sich im gleichen Ordner wie gps-test.py befinden




def gps_test(data_list):
    # Verwendung von enumerate für eine sauberere Schleife
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



# BEISPIELE (Hashtag entfernen zum Ausprobieren):
        dateifunktionen.gps_json_write(coords_str, time_str, parent_folder) # Erzeugt eine neue Datei mit aktueller Zeit als Namen im Ordner parent_folder.
        #dateifunktionen.gps_json_write(coords_str, time_str) # Erzeugt eine neue Datei im gleichen Ordner wie dieses Programm
        #dateifunktionen.gps_json_write (coords, time_str, parent_folder, "Name") # Erzeugt eine neue Datei Name.json in parent_folder
        #dateifunktionen.gps_json_write (coords, time_str, "Name") # Erzeugt eine neue Datei Name.json im gleichen Ordner
        #dateifunktionen.gps_json_write (coords, time_str, "Beispielordner", "Name") # Erzeugt eine neue Datei Name.json im Ordner Beispielordner



# Standorte als Liste ausgeben (bereits nach Anforderungen des Pflichtenheftes sortiert, jeder Standorteintrag besteht aus Koordinatenstring, Name (falls unbenannt: "none") und Timestamp)
print("STANDORTLISTE:")
print(dateifunktionen.get_standorte())