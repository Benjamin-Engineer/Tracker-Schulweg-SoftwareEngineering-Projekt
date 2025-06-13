# Tracker-Schulweg-SoftwareEngineering-Projekt
Repository für das Projekt im Modul "Grundlagen des Software Engineering" über einen Tracker für den Schulweg von Schülern.

dateifunktionen.py

    gps_json_write(Koordinaten, Zeitstempel, "Optional:Ordner", "Optional:Dateiname", "Optional:Culling-Toleranz", "Optional:Standorterkennungszeit")
      Formatiert die angegebenen Koordinaten sowie den Zeitstempel und schreibt sie in eine JSON-Routendatei. Gegebenenfalls wird eine neue Datei erstellt.
      Erkennt Standorte und erstellt automatisch Standortdateien für diese im Standardordner von `erstelle_standortdatei` (siehe weiter unten).
      Standardparameter:
      "Ordner" : der gleiche Ordner wie das ausgeführte Programm.
      "Dateiname" : aktuelle Zeit im Format "YYYY-MM-DD_HH-MM-SS.json".
      "Culling-Toleranz": 0.0001 (entspricht 1,1112 Metern).
      "Standorterkennungszeit": 15 (Angabe in Minuten; 15 Minuten sind im Pflichtenheft spezifiziert).
    
    erstelle_standortdatei(Koordinaten, Zeitstempel, "Optional:Ordner")
        Erstellt eine Standortdatei (.txt) mit den angegebenen Koordinaten und dem Zeitstempel.
        Der Speicherordner kann beim Aufruf angepasst werden (für dieses Projekt nicht notwendig).
        Standardparameter:
        "Ordner" : "Standorte"-Ordner im aktuellen Dateipfad

    benenne_standort(Neuer Name, Dateiname, "Optional:Ordner")
        Weist dem Standort der ausgewählten Standortdatei einen neuen Namen zu.
        Optional kann der Ordner ausgewählt werden, in dem sich die Datei befindet, sollte sie sich nicht im Standardordner befinden.
        Standardparameter:
        "Ordner" : "Standorte"-Ordner im aktuellen Dateipfad

    get_standorte("Optional:Ordner", "Optional:Dateiname") 
        Gibt eine Liste aller Standorte im Standardordner (oder, falls angegeben, im ausgewählten Ordner) zurück.
        Wenn eine Routendatei angegeben wird, werden nur Standorte ausgegeben, welche in der Route vorkommen (die Dateien dieser Standorte müssen im angegebenen Ordner liegen).
        Die Standorte in der Liste werden automatisch gemäß den Anforderungen des Pflichtenhefts sortiert:
        Zuerst alle unbenannten Standorte in chronologischer Reihenfolge, danach alle benannten Standorte in alphabetischer Reihenfolge.
        Die Einträge der Liste haben jeweils das Format (Koordinaten, Name, Zeitstempel), wobei der Eintrag "Name" mit "None" gekennzeichnet ist, wenn der Standort noch nicht benannt wurde (Rot auf der Karte anzeigen).
        Beispiel:
        get_standorte() gibt alle Standorte im Standardordner ("Standorte") zurück.
        get_standorte(None, "2025-06-12\2025-06-12 15-19-38-209885.json") gibt alle Standorte aus, welche in der Route vorkommen und im Standardordner ("Standorte") gespeichert sind.
        Standardparameter:
        "Ordner" : "Standorte"-Ordner im aktuellen Dateipfad - nur Standorte aus dem angegebenen Ordner werden berücksichtigt
        "Dateiname" : Dateipfad einer Routendatei. Falls angegeben, werden nur Standorte (aus dem angegebenen Ordner) ausgegeben, die auch in der Route vorkommen


----------------------------------------------------------------------------------------------------------------------------------------------------------------

  gps.py
      
      Erfasst die vom GPS gesendeten Daten wie Koordinaten und Zeitstempel.

----------------------------------------------------------------------------------------------------------------------------------------------------------------

pin.py 

    Erstellt eine Standard-PIN für das Sicherheitsverfahren über `default_pin()` und speichert diese in einer Textdatei.
    Über get_pin() wird die PIN aus der Datei ausgelesen.
    Vergleicht die eingegebene PIN mit der vorhandenen PIN über `check_pin(entered_pin)`. Hier wird `get_pin()` aufgerufen. Wenn beide übereinstimmen, wird `True` zurückgegeben, sonst `False`.
    Setzt eine neue PIN in der Datei `pin.txt` und überschreibt die alte mit `set_pin(new_pin)`.
    Über `change_pin(alte_pin, new_pin, confirm_pin)` wird die PIN geändert.
    
        Hierfür wird eine Abfrage der alten PIN über `check_pin(alte_pin)` getätigt. Sobald diese korrekt ist, wird die Eingabe einer neuen PIN mit deren 
        Bestätigung ermöglicht. Stimmen beide überein und sind die Kriterien für die PIN erfüllt (nur Ziffern und mindestens 6 Zeichen), wird die PIN 
        über `set_pin(new_pin)` in der Datei `pin.txt` gespeichert und die alte überschrieben.
        Zur Aufklärung: Die Variable `alte_pin` wird für die aktuell noch gespeicherte PIN genutzt, `new_pin` ist dann die gewünschte neue PIN und `confirm_pin` ist die wiederholte Eingabe der neuen PIN als Sicherheitsschritt.

    Daraus folgt, dass `default_pin()` zu Beginn ausgeführt werden muss, am besten direkt beim Starten des Geräts.

    
planner.py

    Über `load_entries()` werden die Einträge des Planers aus der JSON-Datei geladen.
    Die Funktion `save_entries(startzeit, endzeit)` erweitert die bestehende Liste um das hinzugefügte Element (von, bis). Die Einträge werden, sortiert nach "von", an die JSON-Datei übergeben.
    Über `show_planner_entries()` wird auf die Funktion `load_entries()` zugegriffen und die Visualisierung der Liste ermöglicht.


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

start_stop.py

    Hinzufügen einer Toggle-Funktion für die Start-Stopp-Aktivität.

        Falls `is_recording == true` -> aktives Tracking.
        Falls `is_recording == false` -> kein aktives Tracking.


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


shutdown.py

    Hinzufügen einer Funktion zum Herunterfahren des Systems

        Durch das aufrufen von system_shutdown() wird das System direkt heruntergefahren


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------