# Tracker-Schulweg-SoftwareEngineering-Projekt
Repository für das Projekt im Modul Grundlagen des Software Engineering über ein Tracker für den Schulweg von Schülern

pin.py 

    Erstellt eine standard pin für das Sicherheitsverfahren über default_pin() und speichert diese in einer text.file.
    Über get_pin() wird die PIN aus der Datei ausgelesen.
    Vergeleicht eingegebene PIN mit vorhandener pin, über check_pin(entered_pin), hier wurd get_pin() aufgerufen, wenn beide übereinstimmen wird ein True wert zurückgegeben,sonst False
    Setzt einen neuen PIN in der pin.txt Datei und überschreibt den alten, mit set_pin(new_pin) 
    Über change_pin(alte_pin, new_pin, corfim_pin) wird die pin geändert.
    
        hierfür wird eine Abfrage des Alten PIN's über check_pin(alte_pin) getätigt, sobald dieser korrekt ist wird die eingabe eines Neuen pins mit dessen 
        Confirmation ermöglicht. Stimmen beide überein und die Kriterien für den PIN sind erfüllt (nur Nummern und mindestens 6 zeichen), wird die PIN 
        über set_pin(new_pin) in die pin.txt datei gespeichert und die Alte überschrieben.
        Zur aufklärung, die variable alte_pin wird für die Aktuelle noch gespeicherte PIN genutzt new_pin ist dann die gewünschte neue PIN und mit confirm_pin ist die neue PIN nur wiederholt als sicherheits schritt.

    Daraus folgt, dass die default_pin() zu beginn laufen muss, am besten direkt beim starten des Gerätes.

    
planner.py

    Über load_entries() werden die einträge des Planners aus der JSON-Datei geladen.
    Die funktion save_entries(startzeit, endzeit) erweitert die bestehende Liste um das hinzugefügte element (von, bis). Die einträge werden Sortiert nach "von" an die JSON-Datei übergeben.
    Über show_planner_entries(), wird auf die Funktion load_entries() zugegriffen und die visualisierung der Liste ermöglicht.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
