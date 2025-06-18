import json
import os # path operations & folder creation
from datetime import datetime, timedelta, timezone

import shutil # For deleting directories



# STANDARDWERTE:

STANDORTE_FOLDER = "Standorte"  # Standardordner für Standortdateien
# Ordner wird von der gleichen Stelle erstellt, wo sich die ausgeführte Datei befindet

POSITION_CULLING = 0.0005 # Standardwert für die minimale Distanz zur letzten Position, um einen neuen Eintrag zu erstellen
# 0.00001 = 0.11112m <-> 0.0001 = 1.1112m <-> 0.001 = 11.112m (laut https://wiki.openstreetmap.org/wiki/Precision_of_coordinates)

STANDORT_DEFINITION = 15 # Standardwert für die Dauer (in Minuten), für die keine signifikante Bewegung festgestellt wird, bis die Position als Standort erkannt wird
# Standardwert 15, da 15 Minutes im Pflichtenheft steht (kann zu Testzwecken reduziert werden)





def erstelle_standortdatei(coordinates_str, timestamp_str, folder=STANDORTE_FOLDER):
    """
    Erstellt eine Textdatei für einen Standort, wenn diese noch nicht existiert.
    Die Datei wird nach den Koordinaten benannt und enthält die Koordinaten und den Zeitstempel.

    Args:
        coordinates_str (str): Die Koordinaten als String (z.B. "50.742708 7.066977").
        timestamp_str (str): Der Zeitstempel als String (z.B. "2023-10-27 15:30:00.123456").
        folder (str, optional): Der Ordner, in dem die Datei gespeichert werden soll.
                                Standardmäßig "Standorte".
    """
    # Ersetze ungültige Zeichen für Dateinamen, falls Koordinaten Sonderzeichen enthalten (z.B. bei "NO SIGNAL")
    # Windows verbietet < > : " / \ | ? *
    # Linux verbietet / und Null-Byte. os.path.join kümmert sich um /
    safe_filename_part = coordinates_str.replace(":", "-").replace("/", "-").replace("\\", "-")
    safe_filename_part = "".join(c for c in safe_filename_part if c not in '<>"|?*')

    filename = f"{safe_filename_part}.txt"
    full_path_to_file = os.path.join(folder, filename)

    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Info: Ordner '{folder}' für Standortdateien wurde erstellt.")
        
        if os.path.exists(full_path_to_file):
            print(f"Info: Standortdatei '{full_path_to_file}' existiert bereits und wird nicht überschrieben.")
            return

        with open(full_path_to_file, 'w', encoding='utf-8') as f:
            f.write(f"{coordinates_str}\n")
            f.write(f"{timestamp_str}\n")
        print(f"Info: Standortdatei '{full_path_to_file}' wurde erfolgreich erstellt.")
    except OSError as e:
        print(f"Fehler: Konnte Standortdatei '{full_path_to_file}' nicht erstellen/schreiben: {e}")





def benenne_standort(new_name_str, filename_str, folder=STANDORTE_FOLDER):
    """
    Ändert die erste Zeile (den Namen/Koordinaten) einer bestehenden Standort-Textdatei.

    Args:
        new_name_str (str): Der neue Name/Wert für die erste Zeile.
        filename_str (str): Der Dateiname der zu ändernden .txt-Datei (z.B. "50.123456 7.123456.txt").
        folder (str, optional): Der Ordner, in dem sich die Datei befindet.
                                Standardmäßig "Standorte".
    """
    full_path_to_file = os.path.join(folder, filename_str)

    if not os.path.exists(full_path_to_file):
        print(f"Fehler: Datei '{full_path_to_file}' nicht gefunden. Umbenennung nicht möglich.")
        return

    try:
        with open(full_path_to_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            # Wenn die Datei leer ist, erstellen wir die erste Zeile und fügen ggf. eine Leerzeile für den Zeitstempel hinzu
            lines.append(new_name_str + '\n')
            if len(lines) < 2: # Sicherstellen, dass es Platz für einen Zeitstempel gibt
                 lines.append('\n') 
            print(f"Warnung: Datei '{full_path_to_file}' war leer. Erste Zeile wurde zu '{new_name_str}' gesetzt.")
        else:
            # Ersetze die erste Zeile, behalte den Zeilenumbruch bei, falls vorhanden
            original_first_line_had_newline = lines[0].endswith('\n')
            lines[0] = new_name_str + ('\n' if original_first_line_had_newline else '')
            if len(lines) < 2: # Falls die Datei nur eine Zeile hatte, füge eine Leerzeile für den Zeitstempel hinzu
                lines.append('\n')


        with open(full_path_to_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Info: Erste Zeile von '{full_path_to_file}' wurde zu '{new_name_str}' geändert.")

    except IOError as e:
        print(f"Fehler: Konnte Datei '{full_path_to_file}' nicht lesen/schreiben: {e}")
    except Exception as e_general:
        print(f"Ein unerwarteter Fehler ist beim Umbenennen des Standorts in '{full_path_to_file}' aufgetreten: {e_general}")




def _parse_coord_string_to_floats(coord_str):
    """
    Parst einen Koordinaten-String ("lat lon") in zwei Float-Werte.
    Gibt (lat, lon) oder (None, None) bei Fehler zurück.
    """
    try:
        parts = coord_str.split()
        if len(parts) == 2:
            lat = float(parts[0])
            lon = float(parts[1])
            return lat, lon
        return None, None
    except ValueError:
        return None, None



def get_standorte(folder=STANDORTE_FOLDER, routendatei=None):
    """
    Gibt eine Liste aller .txt-Dateien (Standorte) im angegebenen Ordner zurück.
    Jedes Element der Liste ist ein Tupel: (Location, CustomName, Timestamp).
    - Location: Name der .txt-Datei ohne Endung.
    - CustomName: Inhalt der ersten Zeile der .txt-Datei. Ist None, wenn die erste Zeile identisch zur Location ist oder fehlt.
    - Timestamp: Inhalt der zweiten Zeile der .txt-Datei.

    Die Liste ist sortiert:
    1. Standorte ohne CustomName (None), sortiert nach Timestamp (neueste zuerst).
    2. Standorte mit CustomName, sortiert alphabetisch nach CustomName.

    Wenn 'routendatei' (Pfad zu einer JSON-Datei) angegeben ist, werden nur Standorte zurückgegeben,
    deren Koordinaten in der Routendatei enthalten sind (exakt oder nächstgelegen innerhalb von POSITION_CULLING).
    Für Routenpunkte, die keinen passenden Standort finden, wird eine Meldung ausgegeben.
    """
    standort_daten_from_folder = []

    if not os.path.exists(folder):
        print(f"Warnung: Ordner '{folder}' für Standorte nicht gefunden.")
        return []

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            location_from_filename = filename[:-4]  # Dateiname ohne .txt
            
            custom_name = None  # Standardwert
            timestamp_str = ""    # Standardwert

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f.readlines()]
                
                if len(lines) >= 1:
                    first_line_content = lines[0]
                    if first_line_content == location_from_filename:
                        custom_name = None
                    else:
                        custom_name = first_line_content
                # Wenn lines < 1, bleibt custom_name None

                if len(lines) >= 2:
                    timestamp_str = lines[1]
                # Wenn lines < 2, bleibt timestamp_str ""
                
                standort_daten_from_folder.append({
                    "location": location_from_filename,
                    "custom_name": custom_name,
                    "timestamp": timestamp_str,
                    "original_filename": filename # Für Debugging-Zwecke bei Zeitstempel-Parsing
                })

            except IOError as e:
                print(f"Fehler beim Lesen der Datei '{filepath}': {e}")
            except Exception as e_general:
                print(f"Unerwarteter Fehler beim Verarbeiten der Datei '{filepath}': {e_general}")

    standort_daten_to_process = []

    if not routendatei:
        standort_daten_to_process = standort_daten_from_folder
    else:
        if not os.path.exists(routendatei):
            print(f"Warnung: Routendatei '{routendatei}' nicht gefunden. Es werden keine Standorte zurückgegeben.")
            return []

        try:
            with open(routendatei, 'r', encoding='utf-8') as f_route:
                route_entries = json.load(f_route)
            if not isinstance(route_entries, list):
                print(f"Warnung: Inhalt von Routendatei '{routendatei}' ist keine Liste. Keine Standorte können gefiltert werden.")
                return []
        except json.JSONDecodeError:
            print(f"Warnung: Routendatei '{routendatei}' enthält ungültiges JSON. Keine Standorte können gefiltert werden.")
            return []
        except Exception as e:
            print(f"Fehler beim Lesen der Routendatei '{routendatei}': {e}")
            return []

        added_standort_filenames = set() # Verhindert Duplikate, falls mehrere Routenpunkte auf denselben Standort zeigen.
        DISTANCE_THRESHOLD = POSITION_CULLING

        for route_entry in route_entries:
            route_coord_str = route_entry.get("coord")
            route_time_str = route_entry.get("time", "N/A") # Zeitstempel aus der Routendatei für die Meldung.

            if not route_coord_str:
                continue # Routen-Eintrag ohne Koordinaten überspringen

            route_lat, route_lon = _parse_coord_string_to_floats(route_coord_str)
            if route_lat is None or route_lon is None:
                print(f"Info: Route-Koordinaten '{route_coord_str}' konnten nicht geparst werden.")
                continue

            matched_standort_in_folder = None

            # 1. Exakte Übereinstimmung prüfen.
            for s_data in standort_daten_from_folder:
                if s_data["location"] == route_coord_str:
                    matched_standort_in_folder = s_data
                    break

            # 2. Wenn keine exakte Übereinstimmung, nach nächstgelegenem innerhalb der Toleranz suchen
            if not matched_standort_in_folder:
                closest_s_data_within_threshold = None
                min_diff_metric = float('inf')

                for s_data in standort_daten_from_folder:
                    s_loc_str = s_data["location"]
                    s_lat, s_lon = _parse_coord_string_to_floats(s_loc_str)
                    if s_lat is None or s_lon is None:
                        continue 
            
                    lat_diff = abs(route_lat - s_lat)
                    lon_diff = abs(route_lon - s_lon)
            
                    if lat_diff < DISTANCE_THRESHOLD and lon_diff < DISTANCE_THRESHOLD:
                        current_diff_metric = lat_diff**2 + lon_diff**2 
                        if current_diff_metric < min_diff_metric:
                            min_diff_metric = current_diff_metric
                            closest_s_data_within_threshold = s_data
                matched_standort_in_folder = closest_s_data_within_threshold

            if matched_standort_in_folder:
                if matched_standort_in_folder["original_filename"] not in added_standort_filenames:
                    standort_daten_to_process.append(matched_standort_in_folder)
                    added_standort_filenames.add(matched_standort_in_folder["original_filename"])
            else:
                print(f"Location {route_coord_str} (Timestamp: {route_time_str}) from route file is not present as a standort in '{folder}'.")

    unnamed_standorte = []
    named_standorte = []
    for item in standort_daten_to_process:
        if item["custom_name"] == None:
            unnamed_standorte.append(item)
        else:
            named_standorte.append(item)

    # Sortierfunktion für unbenannte Standorte (nach Zeitstempel, neueste zuerst)
    def get_sort_key_unnamed(item):
        ts_str = item["timestamp"]
        if not ts_str: # Leerer Zeitstempel wird als ältester behandelt.
            return datetime.min.replace(tzinfo=timezone.utc)
        try:
            return _parse_string_to_utc_datetime(ts_str)
        except ValueError:
            # print(f"Warnung: Zeitstempel '{ts_str}' für '{item['original_filename']}' konnte nicht geparst werden. Wird als ältester sortiert.")
            return datetime.min.replace(tzinfo=timezone.utc) # Bei Fehler als ältester

    unnamed_standorte.sort(key=get_sort_key_unnamed, reverse=True)

    # Sortierfunktion für benannte Standorte (alphabetisch nach Custom Name)
    named_standorte.sort(key=lambda item: item["custom_name"].lower())

    # Erstelle die finale Ergebnisliste im gewünschten Tupel-Format
    ergebnisliste = []
    for item in unnamed_standorte:
        ergebnisliste.append((item["location"], item["custom_name"], item["timestamp"]))
    
    for item in named_standorte:
        ergebnisliste.append((item["location"], item["custom_name"], item["timestamp"]))
        
    return ergebnisliste





def _parse_string_to_utc_datetime(ts_str):
    """
    Parst verschiedene Zeitstempel-Stringformate in zeitzonenbewusste datetime-Objekte (UTC).
    Behandelt Formate wie:
    - "JJJJ-MM-TT HH:MM:SS.ffffff" (von str(datetime.now()) oder ähnlichen Formaten ohne explizite Zeitzone)
    - "JJJJ-MM-TT HH:MM:SS+HH:MM" (ISO mit Zeitzone)
    - "JJJJ-MM-TT HH:MM:SS+HH.MM" (Variante aus Testdaten, wird konvertiert)
    """
    original_ts_str = ts_str # Für Fehlermeldungen.

    # Übliche Vorverarbeitung
    if 'T' not in ts_str and ' ' in ts_str: # Stellt sicher, dass 'T' als Trennzeichen für ISO-Format verwendet wird.
        ts_str = ts_str.replace(' ', 'T', 1)
    if len(ts_str) > 6 and ts_str[-3] == '.' and (ts_str[-6] == '+' or ts_str[-6] == '-'): # Korrigiert +HH.MM zu +HH:MM
        ts_str = ts_str[:-3] + ":" + ts_str[-2:]

    dt_obj = None
    try:
        dt_obj = datetime.fromisoformat(ts_str)
    except ValueError:
        formats_to_try = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"]
        for fmt in formats_to_try:
            try:
                dt_obj = datetime.strptime(ts_str, fmt)
                break 
            except ValueError:
                continue
        if dt_obj is None:
            raise ValueError(f"Zeitstempel-String '{original_ts_str}' konnte mit keinem bekannten Format geparst werden.")

    if dt_obj.tzinfo is None or dt_obj.tzinfo.utcoffset(dt_obj) is None:
        # Macht das Objekt zeitzonenbewusst mit der lokalen Zeitzone und konvertiert dann zu UTC
        dt_obj = dt_obj.astimezone().astimezone(timezone.utc)
    else:
        # Wenn bereits zeitzonenbewusst, nur zu UTC konvertieren
        dt_obj = dt_obj.astimezone(timezone.utc)
    return dt_obj

def parse_and_format_to_short_timestamp_string(ts_str):
    """
    Parst verschiedene Zeitstempel-Stringformate und gibt einen formatierten String "JJJJ-MM-TT HH:MM:SS" zurück.
    Die Zeit wird vor der Formatierung in UTC konvertiert.
    """
    try:
        datetime_obj_utc = _parse_string_to_utc_datetime(ts_str)
        return datetime_obj_utc.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print(f"Warnung: Konnte Zeitstempel '{ts_str}' nicht für Kurzformatierung parsen: {e}")
        # Entscheide über Fallback-Verhalten: erneut auslösen, Original zurückgeben oder Fehlerstring zurückgeben
        # Vorerst wird erneut ausgelöst, um den Aufrufer auf das Parsing-Problem aufmerksam zu machen.
        raise



def gps_json_write(coordinates_str, timestamp_str,  folder=".", filename=str(datetime.now()).replace(":", "-").replace(".", "-") + ".json", culling_accuracy=POSITION_CULLING, standorterkennungszeit=STANDORT_DEFINITION):
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
        culling_accuracy (float, optional): Minimale Distanz (in Grad) zur letzten Position, um einen neuen Eintrag zu erstellen.
        standorterkennungszeit (int, optional): Dauer (in Minuten) ohne signifikante Bewegung, bis ein Standort erkannt wird.
    """

    original_coordinates_str = coordinates_str  # Behält die ursprünglichen Koordinaten für Nachrichten bei.

    final_coord_str_to_write = original_coordinates_str  # Standardwert, falls nicht parsenbar.
    current_f_lat, current_f_lon = None, None
    is_current_coord_valid_for_comparison = False

    # Versucht, original_coordinates_str zu parsen und auf 6 Dezimalstellen zu formatieren. (6 Nachkommastellen sind auf 0.11112m genau, laut https://wiki.openstreetmap.org/wiki/Precision_of_coordinates)
    # Erhält auch Float-Versionen dieser Werte mit 6 Dezimalstellen für den Vergleich.
    try:
        raw_lat_str, raw_lon_str = original_coordinates_str.split()
        raw_lat = float(raw_lat_str)
        raw_lon = float(raw_lon_str)

        final_coord_str_to_write = f"{raw_lat:.6f} {raw_lon:.6f}"
        current_f_lat = float(f"{raw_lat:.6f}") # Float aus der 6-Dezimalstellen-Darstellung.
        current_f_lon = float(f"{raw_lon:.6f}") # Float aus der 6-Dezimalstellen-Darstellung.
        is_current_coord_valid_for_comparison = True
    except ValueError:
        print (f"Info: Eingabe '{original_coordinates_str}' enthält keine validen Koordinaten und wird unaufbereitet übernommen.")

    # Stellt sicher, dass der Zielordner existiert, erstellt ihn, falls nicht.
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
            print(f"Info: Ordner '{folder}' wurde erstellt.")
        except OSError as e:
            print(f"Fehler: Konnte Ordner '{folder}' nicht erstellen: {e}")
            return # Beenden, wenn die Ordnererstellung fehlschlägt.

    full_path = os.path.join(folder, filename)
    existing_data = []

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
            if isinstance(loaded_data, list):
                existing_data = loaded_data
            else:
                print(f"Warnung: Datei {full_path} enthielt keine Liste. Eine neue Liste wird erstellt.")
    except FileNotFoundError:
        print(f"Info: Datei {full_path} nicht gefunden. Eine neue Datei wird erstellt.")
    except json.JSONDecodeError:
        print(f"Warnung: Datei {full_path} enthielt ungültiges JSON oder war leer. Eine neue Liste wird erstellt.")
    except Exception as e:
        print(f"Fehler beim Lesen der JSON-Datei {full_path}: {e}")

    # Prüft auf Abweichung, wenn aktuelle Koordinaten für den Vergleich gültig sind und vorherige Daten vorhanden sind.
    if is_current_coord_valid_for_comparison and existing_data:
        last_entry = existing_data[-1]
        last_coords_str_from_file = last_entry.get("coord")

        if last_coords_str_from_file:
            try:
                # Vorherige Koordinaten aus der Datei (sollten bereits 6 Dezimalstellen haben, wenn gültig).
                last_lat_str_ff, last_lon_str_ff = last_coords_str_from_file.split() # ff = from file / aus Datei.
                last_f_lat = float(last_lat_str_ff)
                last_f_lon = float(last_lon_str_ff)

                if abs(current_f_lat - last_f_lat) < culling_accuracy and abs(current_f_lon - last_f_lon) < culling_accuracy:
                    print(f"Info: Neuer Eintrag (Original: '{original_coordinates_str}', Formatiert: '{final_coord_str_to_write}') weicht minimal von letztem Eintrag ('{last_coords_str_from_file}') ab. Eintrag wird übersprungen.")
                    return # Fügt den neuen Eintrag nicht hinzu.
            except ValueError:
                # Die letzte Koordinate in der Datei war kein gültiges, parsenbares Paar (z.B. "NO SIGNAL").
                # Fährt fort, die neue hinzuzufügen, wenn sie gültig ist.
                pass

    # Prüfe auf signifikante Zeitlücke zum vorherigen Eintrag, um eine Standortdatei zu erstellen
    if existing_data: # Sicherstellen, dass es einen vorherigen Eintrag zum Vergleichen gibt
        last_written_entry = existing_data[-1]
        last_timestamp_str_from_file = last_written_entry.get("time")
        current_timestamp_to_evaluate = timestamp_str # Zeitstempel des aktuellen, potenziellen Eintrags

        if last_timestamp_str_from_file and current_timestamp_to_evaluate:
            try:
                last_dt_utc = _parse_string_to_utc_datetime(last_timestamp_str_from_file)
                current_dt_utc = _parse_string_to_utc_datetime(current_timestamp_to_evaluate)
                
                time_difference = current_dt_utc - last_dt_utc

                if time_difference >= timedelta(minutes=standorterkennungszeit):
                    coords_for_standort = last_written_entry.get("coord")
                    if coords_for_standort and coords_for_standort != "NO SIGNAL": # Nur Standortdatei erstellen, wenn Koordinate valide ist
                        print(f"Info: Zeitdifferenz von {time_difference} zum letzten Eintrag ({last_timestamp_str_from_file}) erkannt. Erstelle Standortdatei für vorherige Koordinate '{coords_for_standort}' mit Zeitstempel des neuen Eintrags '{current_timestamp_to_evaluate}'.")
                        erstelle_standortdatei(coordinates_str=coords_for_standort,
                                               timestamp_str=current_timestamp_to_evaluate)
                    elif coords_for_standort == "NO SIGNAL":
                        print(f"Info: Zeitdifferenz von {time_difference} erkannt, aber vorherige Koordinate war 'NO SIGNAL'. Keine Standortdatei erstellt.")
                    else:
                        print(f"Warnung: Konnte keine Koordinaten im vorherigen Eintrag für Standortdatei finden.")

            except ValueError as e_parse:
                print(f"Warnung: Zeitstempel '{last_timestamp_str_from_file}' oder '{current_timestamp_to_evaluate}' konnte für Zeitdifferenzprüfung nicht geparst werden: {e_parse}")
            except Exception as e_general: 
                print(f"Ein unerwarteter Fehler ist bei der Zeitdifferenzprüfung aufgetreten: {e_general}")

    new_entry = {
        "coord": final_coord_str_to_write,
        "time": timestamp_str
    }
    existing_data.append(new_entry)
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2)
        print(f"Eintrag erfolgreich zu {full_path} hinzugefügt.")
    except IOError as e:
        print(f"Fehler beim Schreiben in Datei {full_path}: {e}")
    except Exception as e_general:
        print(f"Ein unerwarteter Fehler ist beim Schreiben der JSON-Datei {full_path} aufgetreten: {e_general}")



def delete_routes(alter_in_tagen=100, base_folder="."):
    """
    Löscht alle Routenordner (und deren Inhalt) im base_folder, die älter 
    als 'alter_in_tagen' sind.
    Routenordner werden anhand ihres Namens identifiziert, der einem Datumsmuster 
    (YYYY-MM-DD) entsprechen muss.

    Args:
        alter_in_tagen (int): Das maximale Alter der Ordner in Tagen. Ordner, die älter sind, werden gelöscht.
        base_folder (str, optional): Der Basisordner, in dem nach Routenordnern gesucht wird. 
                                     Standardmäßig der aktuelle Ordner (".").
    """
    if not os.path.isdir(base_folder):
        print(f"Fehler: Der angegebene Basisordner '{base_folder}' existiert nicht oder ist kein Ordner.")
        return

    heute = datetime.now().date()
    print(f"INFO: Suche nach Routenordnern älter als {alter_in_tagen} Tage im Ordner '{os.path.abspath(base_folder)}'...")

    for item_name in os.listdir(base_folder):
        item_path = os.path.join(base_folder, item_name)
        if os.path.isdir(item_path):
            try:
                folder_date = datetime.strptime(item_name, "%Y-%m-%d").date()
                if (heute - folder_date).days > alter_in_tagen:
                    print(f"INFO: Lösche Ordner '{item_path}', da er {(heute - folder_date).days} Tage alt ist (älter als {alter_in_tagen} Tage).")
                    shutil.rmtree(item_path)
                    print(f"INFO: Ordner '{item_path}' erfolgreich gelöscht.")
            except ValueError:
                # Ordnername entspricht nicht dem Datumsformat YYYY-MM-DD, wird ignoriert.
                pass
            except Exception as e:
                print(f"Fehler beim Löschen des Ordners '{item_path}': {e}")