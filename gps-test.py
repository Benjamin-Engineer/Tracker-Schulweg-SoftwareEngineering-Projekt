import datetime
import dateifunktionen # Benutzerdefinierter Import. Kann fehlschlagen, wenn dateifunktionen.py umbenannt wird.
import os # Für Pfadoperationen wie os.path.join und os.path.exists
import teststandorte_generieren


# VOREINSTELLUNGEN.

# Welche Testdatendatei soll verwendet werden? (die Testdatendatei sollte echte erfasste Rohdaten für eine Route oder simulierte Daten im gleichen Format enthalten)
listendatei = "testdaten_extrapoliert.txt"
#listendatei = "testdaten.txt"

# Sollen die erfassten Testdaten in der Konsole ausgegeben werden? (um zu überprüfen, ob die Testdatendatei richtig erkannt und gelesen wird - ziemlich viele Zeilen, also Standardmäßig aus)
zeige_testdaten_in_konsole = False

# Sollen Teststandorte erstellt werden? (Standorte, die in einer Route erkannt werden, werden immer automatisch erstellt - es geht vielmehr darum, get_standorte() zu demonstrieren und zu testen, dass gps_json_write() vorhandene Standorte richtig erkennt & keine Duplikate erzeugt)
teststandorte_erstellen = True

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


# Gibt die Liste der Daten über print() aus. Nummerierung ist in der json nicht vorhanden
if zeige_testdaten_in_konsole:
    if daten:
        for i, item in enumerate(daten):
            print(i, item)
    else:
        print(listendatei, "enthält keine Daten.")


if teststandorte_erstellen: # kann in den Voreinstellungen angepasst werden
    # Erstellt zum Testen Standortdateien, darunter auch eine bereits benannte Standortdatei, welche in der Testroute vorkommt
    teststandorte_generieren.erstelle_test_standortdateien()

# Definiert den Ordner für die Routen-JSON-Datei.
parent_folder = str(datetime.date.today())

# Definiert den Ziel-JSON-Dateinamen *einmal* vor der Haupt-Datenverarbeitungsschleife.
# Dies stellt sicher, dass alle Einträge aus 'daten' in eine einzige, bekannte Datei für den Test gelangen.
route_filename_for_test = str(datetime.datetime.now()).replace(":", "-").replace(".", "-") + ".json"
full_route_filepath = os.path.join(parent_folder, route_filename_for_test)

"""
Dieser Abschnitt fügt alle Koordinaten-Paare aus der Liste 'daten' 
mit den zugehörigen Zeitstempeln (aus der Testdatendatei generiert) 
zu einer spezifischen Routendatei hinzu (definiert als full_route_filepath).
"""
if daten:
    print(f"\nINFO: Writing GPS data to route file: {full_route_filepath}")
    for i in range(0, len(daten), 2):
        coords_str = daten[i]
        time_str = daten[i+1]

# BEISPIELE (Hashtag entfernen zum Ausprobieren):
        # Der primäre Aufruf verwendet nun einen expliziten Dateinamen für den Test.
        dateifunktionen.gps_json_write(coords_str, time_str, folder=parent_folder, filename=route_filename_for_test)
        
        #dateifunktionen.gps_json_write(coords_str, time_str) # Erzeugt eine neue Datei im gleichen Ordner wie dieses Programm
        #dateifunktionen.gps_json_write (coords, time_str, parent_folder, "Name") # Erzeugt eine neue Datei Name.json in parent_folder
        #dateifunktionen.gps_json_write (coords, time_str, "Name") # Erzeugt eine neue Datei Name.json im gleichen Ordner
        #dateifunktionen.gps_json_write (coords, time_str, "Beispielordner", "Name") # Erzeugt eine neue Datei Name.json im Ordner Beispielordner
else:
    print(f"\nINFO: No data in '{listendatei}', so no route file will be generated at '{full_route_filepath}'.")


def test_get_standorte_with_routefile(route_file_path_to_test):
    """Testet dateifunktionen.get_standorte mit einer spezifischen Routendatei."""
    print("\n--- get_standorte für spezifische Route: ---")
    if not os.path.exists(route_file_path_to_test):
        print(f"FEHLER: Routendatei '{route_file_path_to_test}' nicht gefunden. Test kann nicht durchgeführt werden.")
        return

    print(f"INFO: Using route file: {route_file_path_to_test} to filter Standorte.")
    standorte_gefiltert = dateifunktionen.get_standorte(routendatei=route_file_path_to_test)


    print("\nErgebnis von get_standorte (gefiltert nach Route):")
    if standorte_gefiltert:
        for standort_tuple in standorte_gefiltert: # Renamed to avoid conflict if 'standort' is a module
            print(standort_tuple) # Umbenannt, um Konflikte zu vermeiden, falls 'standort' ein Modul ist.
    else:
        print("Keine Standorte gefunden oder passend zur Route.")


# Standorte als Liste ausgeben (bereits nach Anforderungen des Pflichtenheftes sortiert, jeder Standorteintrag besteht aus Koordinatenstring, Name (falls unbenannt: "none") und Timestamp)

# Ruft die neue Testfunktion für get_standorte mit der generierten Routendatei auf.
if daten: # Führt diesen Test nur aus, wenn Daten verarbeitet wurden und die Datei erstellt werden sollte.
    test_get_standorte_with_routefile(full_route_filepath)
else:
    print(f"\nINFO: Skipping test_get_standorte_with_routefile as no data was processed to create {full_route_filepath}.")

print("\nSTANDORTLISTE (alle Standorte aus dem Standardordner):")
print(dateifunktionen.get_standorte())

print("\nLösche Routen, die älter sind als (Zeit in Tagen angeben; gestern = älter als 0 Tage, heute = älter als -1 Tage): ")
alter = input()
try:
    dateifunktionen.delete_routes(alter_in_tagen=int(alter))
except:
    print("delete_routes-Test abgebrochen: ungültige Eingabe")

print("\nCHRONOLOGISCHE ROUTENLISTE (alle verfügbaren Routen, sortiert nach Datum):")
try:
    alle_routen = dateifunktionen.get_all_routes_sorted()
    if alle_routen:
        print(f"Insgesamt {len(alle_routen)} Routen gefunden:")
        for route_info in alle_routen:
            print(f"  - {route_info['display_name']}")
            print(f"    Pfad: {route_info['file_path']}")
    else:
        print("Keine Routen gefunden.")
except Exception as e:
    print(f"Fehler beim Laden der chronologischen Routenliste: {e}")

print("\nVERFÜGBARE DATUMSORDNER:")
try:
    datumsordner = dateifunktionen.get_all_route_folders()
    if datumsordner:
        print(f"Insgesamt {len(datumsordner)} Datumsordner mit Routen gefunden:")
        for ordner_pfad, ordner_datum, ordner_name in datumsordner:
            json_dateien = [f for f in os.listdir(ordner_pfad) if f.endswith('.json')]
            print(f"  - {ordner_name} ({len(json_dateien)} Routen)")
    else:
        print("Keine Datumsordner mit Routen gefunden.")
except Exception as e:
    print(f"Fehler beim Laden der Datumsordner: {e}")